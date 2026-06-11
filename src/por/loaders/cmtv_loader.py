import re
import httpx
import asyncio
import stamina

from parsel import Selector
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

from rage.meta.interfaces import Document, TextLoader


LYRICS_PARAGRAPH_XPATH = (
    "//h4[contains(concat(' ', normalize-space(@class), ' '), ' letra ')]"
    "/parent::header/following-sibling::p[1]"
)


@stamina.retry(on=httpx.HTTPError, wait_initial=10, wait_max=60, attempts=10)
async def _get_req(url: str) -> httpx.Response:
    async with httpx.AsyncClient(
        follow_redirects=True,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
        },
    ) as client:
        resp = await client.get(url)
        resp.raise_for_status()

        return resp


class CMTVLoader(TextLoader):
    def __init__(self, max_concurrency: int = 2):
        super().__init__()
        self.semaphore = asyncio.Semaphore(max_concurrency)

    @staticmethod
    def _is_disk_url(url: str) -> bool:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        return (
            parsed_url.path.endswith("/discos_letras/show.php")
            and "DS_DS" in query_params
        )

    @staticmethod
    def _is_song_url(url: str) -> bool:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        return (
            parsed_url.path.endswith("/discos_letras/letra.php")
            and "bnid" in query_params
            and "tmid" in query_params
        )

    @staticmethod
    def _has_same_query_value(url: str, source_url: str, key: str) -> bool:
        url_values = parse_qs(urlparse(url).query).get(key, [])
        source_values = parse_qs(urlparse(source_url).query).get(key, [])

        return bool(
            url_values and source_values and url_values[0] == source_values[0]
        )

    @staticmethod
    def _normalize_url(url: str) -> str:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        encoded_query = urlencode(
            {key: values[0] for key, values in query_params.items() if values}
        )

        return urlunparse(parsed_url._replace(query=encoded_query))

    @staticmethod
    def _clean_text(parts: list[str]) -> str:
        text = "\n".join(part.strip() for part in parts if part.strip())

        return re.sub(r"\n{3,}", "\n\n", text).strip()

    @staticmethod
    def _clean_lyrics_html(html: str) -> str:
        html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
        text = Selector(text=html).xpath("string()").get(default="")
        lines = (
            re.sub(r"[ \t\f\v]+", " ", line).strip()
            for line in text.splitlines()
        )
        text = "\n".join(lines)

        return re.sub(r"\n{3,}", "\n\n", text).strip()

    @staticmethod
    def _get_query_value(url: str, key: str) -> str | None:
        values = parse_qs(urlparse(url).query).get(key, [])
        if values:
            return values[0]

        return None

    @classmethod
    def extract_title(cls, html: str) -> str | None:
        selector = Selector(text=html)
        title_candidates = (
            cls._clean_text(selector.css(css).getall())
            for css in (
                "h1::text",
                "h2::text",
                ".titulo::text",
                ".title::text",
                "title::text",
            )
        )

        return next((title for title in title_candidates if title), None)

    @classmethod
    def extract_lyrics(cls, html: str, song_url: str) -> str:
        selector = Selector(text=html)
        lyrics_html = selector.xpath(LYRICS_PARAGRAPH_XPATH).get()
        if lyrics_html is not None:
            return cls._clean_lyrics_html(html=lyrics_html)

        return ""

    @classmethod
    def extract_disk_urls(cls, html: str, source_url: str) -> list[str]:
        selector = Selector(text=html)
        urls = (
            cls._normalize_url(url=urljoin(source_url, href))
            for href in selector.css("a::attr(href)").getall()
        )

        return list(
            dict.fromkeys(
                url
                for url in urls
                if cls._is_disk_url(url=url)
                and cls._has_same_query_value(
                    url=url,
                    source_url=source_url,
                    key="bnid",
                )
            )
        )

    @classmethod
    def extract_song_urls(cls, html: str, source_url: str) -> list[str]:
        selector = Selector(text=html)
        urls = (
            cls._normalize_url(url=urljoin(source_url, href))
            for href in selector.css("a::attr(href)").getall()
        )

        return list(
            dict.fromkeys(
                url
                for url in urls
                if cls._is_song_url(url=url)
                and cls._has_same_query_value(
                    url=url,
                    source_url=source_url,
                    key="bnid",
                )
            )
        )

    async def get_disk_urls(self, artist_url: str) -> list[str]:
        resp = await _get_req(url=artist_url)
        return self.extract_disk_urls(
            html=resp.text,
            source_url=artist_url,
        )

    async def get_song_urls_from_disk(self, disk_url: str) -> list[str]:
        async with self.semaphore:
            resp = await _get_req(url=disk_url)

        return self.extract_song_urls(
            html=resp.text,
            source_url=disk_url,
        )

    async def get_song_urls(self, artist_url: str) -> list[str]:
        disk_urls = await self.get_disk_urls(artist_url=artist_url)
        song_url_groups = await asyncio.gather(
            *(
                self.get_song_urls_from_disk(disk_url=disk_url)
                for disk_url in disk_urls
            )
        )
        song_urls = (
            song_url for song_urls in song_url_groups for song_url in song_urls
        )

        return list(dict.fromkeys(song_urls))

    async def get_document(self, song_url: str) -> Document | None:
        async with self.semaphore:
            resp = await _get_req(url=song_url)

        lyrics = self.extract_lyrics(html=resp.text, song_url=song_url)
        if not lyrics:
            return None

        return Document(
            text=lyrics,
            metadata={
                "title": self.extract_title(html=resp.text),
                "artist": self._get_query_value(
                    url=song_url,
                    key="banda",
                ),
                "collection": "lyrics",
                "language": "Spanish",
                "source_url": song_url,
                "bnid": self._get_query_value(url=song_url, key="bnid"),
                "tmid": self._get_query_value(url=song_url, key="tmid"),
            },
        )

    async def get_documents(
        self,
        source_path: str | None = None,
    ) -> list[Document]:
        assert source_path is not None
        song_urls = await self.get_song_urls(artist_url=source_path)
        documents = await asyncio.gather(
            *(self.get_document(song_url=song_url) for song_url in song_urls)
        )

        return [document for document in documents if document is not None]
