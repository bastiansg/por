from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

import httpx
import stamina
from parsel import Selector


@stamina.retry(on=httpx.HTTPError, wait_initial=10, wait_max=60, attempts=10)
async def _get_req(url: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

        return resp


class CMTVLoader:
    @staticmethod
    def _is_disk_url(url: str) -> bool:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        return (
            parsed_url.path.endswith("/discos_letras/show.php")
            and "DS_DS" in query_params
        )

    @staticmethod
    def _normalize_url(url: str) -> str:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        encoded_query = urlencode(
            {
                key: values[0]
                for key, values in query_params.items()
                if values
            }
        )

        return urlunparse(parsed_url._replace(query=encoded_query))

    @classmethod
    def extract_disk_urls(cls, html: str, source_url: str) -> list[str]:
        selector = Selector(text=html)
        urls = (
            cls._normalize_url(url=urljoin(source_url, href))
            for href in selector.css("a::attr(href)").getall()
        )

        return list(dict.fromkeys(url for url in urls if cls._is_disk_url(url=url)))

    async def get_disk_urls(self, artist_url: str) -> list[str]:
        resp = await _get_req(url=artist_url)
        return self.extract_disk_urls(
            html=resp.text,
            source_url=artist_url,
        )
