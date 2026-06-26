import json
import re
from collections.abc import Iterable

import httpx
import stamina
from parsel import Selector

from rage.meta.interfaces import Document, TextLoader


ASTRO_HOROSCOPE_URL = "https://www.astro.com/horoscope"
PLANET_NAMES = (
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    "TrueNode",
    "Chiron",
)
ZODIAC_SIGNS = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)
ZODIAC_SYMBOLS = {
    "♈": "Aries",
    "♉": "Taurus",
    "♊": "Gemini",
    "♋": "Cancer",
    "♌": "Leo",
    "♍": "Virgo",
    "♎": "Libra",
    "♏": "Scorpio",
    "♐": "Sagittarius",
    "♑": "Capricorn",
    "♒": "Aquarius",
    "♓": "Pisces",
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


class AstroCurrentPlanetsLoader(TextLoader):
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

    @staticmethod
    def _inject_attribute_text(html: str) -> str:
        selector = Selector(text=html)
        for node in selector.css("[alt], [title]"):
            label = node.attrib.get("alt") or node.attrib.get("title")
            if label in ZODIAC_SIGNS or label in ZODIAC_SYMBOLS:
                node.root.tail = (
                    f" {ZODIAC_SYMBOLS.get(label, label)} "
                    f"{node.root.tail or ''}"
                )

        return selector.get()

    @staticmethod
    def _normalize_sign(value: str) -> str:
        return ZODIAC_SYMBOLS.get(value, value)

    @staticmethod
    def _is_section_end(line: str) -> bool:
        return line in {
            "Explanations of the symbols",
            "Chart of the moment",
        }

    @classmethod
    def _take_section(cls, lines: list[str], start: int) -> str:
        end = next(
            (
                index
                for index, line in enumerate(lines[start + 1 :], start=start + 1)
                if cls._is_section_end(line=line) or line.startswith("Chiron ")
            ),
            len(lines) - 1,
        )

        return "\n".join(lines[start : end + 1])

    @classmethod
    def _get_section_texts(cls, html: str) -> list[str]:
        html = cls._inject_attribute_text(html=html)
        selector = Selector(text=html)
        text = cls._clean_text(selector.css("body ::text").getall())
        lines = text.splitlines()
        current_planets_indexes = (
            index
            for index, line in enumerate(lines)
            if line == "Current Planets"
        )

        return [
            cls._take_section(lines=lines, start=index)
            for index in current_planets_indexes
        ]

    @staticmethod
    def _get_timestamp(section_text: str) -> str | None:
        match = re.search(
            r"\d{1,2}-[A-Za-z]{3}-\d{4},\s+\d{1,2}:\d{2}\s+UT/GMT",
            section_text,
        )
        if match:
            return match.group(0)

        return None

    @classmethod
    def _parse_planet_text(cls, text: str, planet_name: str) -> dict | None:
        sign_names = "|".join(ZODIAC_SIGNS)
        sign_symbols = "".join(re.escape(symbol) for symbol in ZODIAC_SYMBOLS)
        pattern = (
            rf"(?P<name>{re.escape(planet_name)})\s+"
            rf"(?:(?P<sign_a>{sign_names}|[{sign_symbols}])\s+)?"
            rf"(?P<degree>\d{{1,2}})\s+"
            rf"(?:(?P<sign_b>{sign_names}|[{sign_symbols}])\s+)?"
            rf"(?P<minutes>\d{{1,2}})'\s*"
            rf"(?P<seconds>\d{{1,2}})\""
            rf"\s*(?P<retrograde>r)?\s*"
            rf"(?P<declination>\d{{1,2}}[ns]\d{{2}})"
        )
        match = re.search(
            pattern=pattern,
            string=text,
        )
        if match is None:
            return None

        sign = match.group("sign_a") or match.group("sign_b")
        if sign is None:
            return None

        return {
            "name": match.group("name"),
            "sign": cls._normalize_sign(value=sign),
            "degree": int(match.group("degree")),
            "minutes": int(match.group("minutes")),
            "seconds": int(match.group("seconds")),
            "retrograde": bool(match.group("retrograde")),
            "declination": match.group("declination"),
        }

    @classmethod
    def extract_data(cls, html: str, source_url: str) -> dict:
        section_texts = cls._get_section_texts(html=html)
        section_text = next(
            (
                text
                for text in section_texts
                if all(name in text for name in ("Sun", "Moon", "Chiron"))
            ),
            "",
        )

        planets = [
            planet
            for planet_name in PLANET_NAMES
            for planet in [
                cls._parse_planet_text(
                    text=section_text,
                    planet_name=planet_name,
                )
            ]
            if planet is not None
        ]

        return {
            "title": "Current Planets",
            "timestamp": cls._get_timestamp(section_text=section_text),
            "planets": planets,
            "source_url": source_url,
        }

    async def get_data(self, source_path: str | None = None) -> dict:
        source_url = source_path or ASTRO_HOROSCOPE_URL
        resp = await _get_req(url=source_url)

        return self.extract_data(html=resp.text, source_url=source_url)

    async def get_documents(
        self,
        source_path: str | None = None,
    ) -> list[Document]:
        data = await self.get_data(source_path=source_path)

        return [
            Document(
                text=json.dumps(data, ensure_ascii=False),
                metadata={
                    "title": data["title"],
                    "timestamp": data["timestamp"],
                    "collection": "current_planets",
                    "language": "English",
                    "source_url": data["source_url"],
                }
                | self.metadata,
            )
        ]
