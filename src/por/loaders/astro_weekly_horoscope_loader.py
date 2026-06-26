import re
import httpx
import stamina

from parsel import Selector
from collections.abc import Iterable

from rage.meta.interfaces import Document, TextLoader


ASTRO_WEEKLY_HOROSCOPE_URL = "https://www.astro.com/cgi/atxgen.cgi?btyp=wh"
SIGN_NAMES = {
    "gen": "General Tendencies",
    "ari": "Aries",
    "tau": "Taurus",
    "gem": "Gemini",
    "can": "Cancer",
    "leo": "Leo",
    "vir": "Virgo",
    "lib": "Libra",
    "sco": "Scorpio",
    "sag": "Sagittarius",
    "cap": "Capricorn",
    "aqu": "Aquarius",
    "pis": "Pisces",
}


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


class AstroWeeklyLoader(TextLoader):
    def __init__(
        self,
        metadata: dict | None = None,
    ):
        super().__init__()
        self.metadata = metadata or {}

    @staticmethod
    def _clean_text(parts: Iterable[str]) -> str:
        lines = (
            re.sub(r"[ \t\f\v]+", " ", part.replace("\xa0", " ")).strip()
            for part in parts
        )

        text = "\n".join(line for line in lines if line)
        return re.sub(r"\n{3,}", "\n\n", text).strip()

    @classmethod
    def extract_week(cls, html: str) -> str | None:
        selector = Selector(text=html)
        text = cls._clean_text(selector.css("#asmain ::text").getall())
        match = re.search(r"Week from .+", text)
        if match:
            return match.group(0)

        return None

    @classmethod
    def extract_documents(cls, html: str, source_url: str) -> list[Document]:
        selector = Selector(text=html)
        week = cls.extract_week(html=html)
        sections = selector.css("div.sign[id]")

        return [
            Document(
                text=text,
                metadata={
                    "title": SIGN_NAMES.get(sign_id, sign_id),
                    "sign_id": sign_id,
                    "week": week,
                    "collection": "weekly_horoscope",
                    "language": "English",
                    "source_url": source_url,
                },
            )
            for section in sections
            for sign_id in [section.attrib.get("id", "")]
            for text in [cls._clean_text(section.css("::text").getall())]
            if sign_id and text
        ]

    async def get_documents(
        self,
        source_path: str | None = None,
    ) -> list[Document]:
        source_url = source_path or ASTRO_WEEKLY_HOROSCOPE_URL
        resp = await _get_req(url=source_url)
        documents = self.extract_documents(
            html=resp.text, source_url=source_url
        )

        return [
            Document(
                text=document.text,
                metadata=document.metadata | self.metadata,
            )
            for document in documents
        ]
