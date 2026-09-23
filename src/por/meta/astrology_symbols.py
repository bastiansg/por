from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile

from cairosvg import svg2png

from por.meta.schema import ZodiacSign

__all__ = ["astrology_symbols_image"]


ZODIAC_SYMBOLS: dict[ZodiacSign, str] = {
    "Aries": "♈︎",
    "Taurus": "♉︎",
    "Gemini": "♊︎",
    "Cancer": "♋︎",
    "Leo": "♌︎",
    "Virgo": "♍︎",
    "Libra": "♎︎",
    "Scorpio": "♏︎",
    "Sagittarius": "♐︎",
    "Capricorn": "♑︎",
    "Aquarius": "♒︎",
    "Pisces": "♓︎",
}


def format_astrology_symbols(
    sun: ZodiacSign | None,
    moon: ZodiacSign | None,
    rising: ZodiacSign | None,
) -> str:
    """Return monochrome symbols for the sun, moon, and rising signs."""
    sun_symbol = ZODIAC_SYMBOLS[sun] if sun is not None else "?"
    moon_symbol = ZODIAC_SYMBOLS[moon] if moon is not None else "?"
    rising_symbol = ZODIAC_SYMBOLS[rising] if rising is not None else "?"

    return " | ".join(
        (
            f"☀︎ {sun_symbol}",
            f"☾ {moon_symbol}",
            f"↑ {rising_symbol}",
        )
    )


@contextmanager
def astrology_symbols_image(
    sun: ZodiacSign | None,
    moon: ZodiacSign | None,
    rising: ZodiacSign | None,
) -> Generator[str, None, None]:
    """Yield a temporary 576-pixel-wide astrology symbols image."""
    symbols = format_astrology_symbols(sun, moon, rising)
    svg = f"""\
<svg xmlns="http://www.w3.org/2000/svg" width="576" height="56" viewBox="0 0 576 56">
  <rect width="576" height="56" fill="white"/>
  <text
    x="0"
    y="39"
    fill="black"
    font-family="DejaVu Sans, sans-serif"
    font-size="34"
    text-anchor="start"
  >{symbols}</text>
</svg>
"""

    with NamedTemporaryFile(suffix=".png", delete=False) as image_file:
        image_path = Path(image_file.name)

    try:
        svg2png(
            bytestring=svg.encode(),
            write_to=str(image_path),
            output_width=576,
        )

        yield str(image_path)
    finally:
        image_path.unlink(missing_ok=True)
