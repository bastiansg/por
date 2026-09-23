from datetime import datetime, timezone
from functools import lru_cache
from typing import Annotated, Literal
from zoneinfo import ZoneInfo

import swisseph as swe
from aiocache import RedisCache
from aiocache.serializers import JsonSerializer
from geopy.geocoders import Nominatim
from more_itertools import unique_everseen
from pydantic import Field
from pydantic_ai import ModelRetry, RunContext, Tool
from qdrant_client import models
from rich.console import Console
from timezonefinder import timezone_at

from por.config import config
from por.db.qdrant import (
    _get_text_chunks,
    hybrid_search,
    retriever,
)
from por.llm_agents.utils import get_astro_weekly_data
from por.meta.schema import ChunkMetadataFilter, TextChunk
from por.multi_agent.console import render_node_detail
from por.utils.tokens import count_t5_tokens

console = Console()


SEARCH_TOP_K = 5
SEARCH_SCORE_THRESHOLD = 0.3
RETRIEVAL_TTL_SECONDS = 900
GEOCODER = Nominatim(user_agent="por-zodiac-chart")
ZODIAC_SIGN_IDS = {
    "Aries": "ari",
    "Taurus": "tau",
    "Gemini": "gem",
    "Cancer": "can",
    "Leo": "leo",
    "Virgo": "vir",
    "Libra": "lib",
    "Scorpio": "sco",
    "Sagittarius": "sag",
    "Capricorn": "cap",
    "Aquarius": "aqu",
    "Pisces": "pis",
}
ZODIAC_SIGNS = tuple(ZODIAC_SIGN_IDS)
ZODIAC_PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

retrieval_cache = RedisCache(
    endpoint=config.redis_host,
    port=config.redis_port,
    db=config.redis_db,
    namespace="retrievals",
    serializer=JsonSerializer(),
)


def count_flux_tokens(
    text: Annotated[
        str,
        Field(description="Text whose FLUX T5 tokens should be counted."),
    ],
) -> int:
    """Count the FLUX T5 tokens in a string.

    Args:
        text: Text whose FLUX T5 tokens should be counted.
    """

    return count_t5_tokens(text, config.t5_tokenizer_name)


async def store_relevant_chunk_ids(
    ctx: RunContext,
    relevant_chunk_ids: Annotated[
        list[str],
        Field(
            description="Relevant chunk_id values ordered by relevance.",
            min_length=1,
        ),
    ],
) -> int:
    """Store relevant chunk IDs for the current retrieval request.

    Args:
        relevant_chunk_ids: Relevant chunk_id values ordered by relevance.
    """

    deps = ctx.deps
    assert deps is not None

    relevant_chunk_ids = list(unique_everseen(relevant_chunk_ids))
    records = await _get_text_chunks(
        collection_name=deps.collection_name,  # type: ignore
        key="chunk_id",
        values=relevant_chunk_ids,
    )

    stored_chunk_ids = {
        record.payload["metadata"]["chunk_id"]
        for record in records
        if record.payload is not None
    }

    missing_chunk_ids = [
        chunk_id
        for chunk_id in relevant_chunk_ids
        if chunk_id not in stored_chunk_ids
    ]

    if missing_chunk_ids:
        error_message = f"Invalid text chunks: {', '.join(missing_chunk_ids)}."
        render_node_detail("retrieval_validation_error", error_message)
        raise ModelRetry(error_message)

    await retrieval_cache.set(
        deps.request_id,  # type: ignore
        relevant_chunk_ids,
        ttl=RETRIEVAL_TTL_SECONDS,
    )

    return len(relevant_chunk_ids)


async def get_relevant_chunk_ids(request_id: str) -> list[str]:
    return await retrieval_cache.get(request_id, default=[])  # type: ignore


async def philosophy_search(
    query: Annotated[
        str,
        Field(
            description="Spanish query to search for relevant philosophy text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Philosophy sources.

    Args:
        query: Spanish query to search for relevant philosophy text chunks.
    """

    return await hybrid_search(
        query=query,
        collection_name="philosophy",
    )


async def satc_search(
    query: Annotated[
        str,
        Field(
            description="English query to search for relevant Sex and the City text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Sex and the City scripts.

    Args:
        query: English query to search for relevant Sex and the City text
            chunks.
    """

    return await hybrid_search(
        query=query,
        collection_name="satc",
    )


async def astrology_search(
    query: Annotated[
        str,
        Field(
            description="Query to search for relevant astrology text chunks."
        ),
    ],
    query_language: Annotated[
        Literal[
            "English",
            "Spanish",
        ],
        Field(
            description="Language of the input query and matching astrology chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Astrology sources.

    Args:
        query: Query to search for relevant astrology text chunks.
        query_language: Language of the input query and matching astrology
            chunks.
    """

    search_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.language",
                match=models.MatchValue(value=query_language),
            )
        ],
    )

    return await hybrid_search(
        query=query,
        collection_name="astrology",
        search_filter=search_filter,
    )


async def get_astro_weekly_general_tendencies() -> str:
    """Return The Weekly Horoscope general tendencies."""

    data = await get_astro_weekly_data()
    document = data["gen"]

    return document.text


async def get_astro_weekly_horoscope_by_sign(
    sign: Annotated[
        Literal[
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
        ],
        Field(description="Zodiac sign to retrieve the weekly horoscope for."),
    ],
) -> str:
    """Return The Weekly Horoscope for a zodiac sign.

    Args:
        sign: Zodiac sign to retrieve the weekly horoscope for.
    """

    data = await get_astro_weekly_data()
    document = data[ZODIAC_SIGN_IDS[sign]]

    return document.text


def _zodiac_position(longitude: float) -> dict[str, float | str]:
    normalized_longitude = longitude % 360
    sign_index = int(normalized_longitude // 30)

    return {
        "longitude": round(normalized_longitude, 6),
        "sign": ZODIAC_SIGNS[sign_index],
        "degree": round(normalized_longitude % 30, 6),
    }


def _planetary_position(
    julian_day: float,
    planet_id: int,
) -> dict[str, float | str | bool]:
    position, _ = swe.calc_ut(
        julian_day,
        planet_id,
        swe.FLG_SWIEPH | swe.FLG_SPEED,
    )

    return {
        **_zodiac_position(position[0]),
        "retrograde": position[3] < 0,
    }


@lru_cache(maxsize=256)
def get_coordinates(
    city: Annotated[
        str,
        Field(description="City of the birthplace.", min_length=1),
    ],
    country: Annotated[
        str,
        Field(description="Country of the birthplace.", min_length=1),
    ],
) -> tuple[float, float]:
    """Resolve a city and country to latitude and longitude.

    Args:
        city: City of the birthplace.
        country: Country of the birthplace.

    Returns:
        Latitude and longitude in decimal degrees.

    Raises:
        ValueError: If the city and country cannot be resolved.
    """

    location = GEOCODER.geocode(
        {
            "city": city,
            "country": country,
        },
        exactly_one=True,
    )

    if location is None:
        raise ValueError(f"Location not found: {city}, {country}")

    return location.latitude, location.longitude


def _localize_datetime(
    local_datetime: datetime,
    latitude: float,
    longitude: float,
) -> tuple[datetime, str]:
    timezone_name = timezone_at(lng=longitude, lat=latitude)

    if timezone_name is None:
        raise ValueError("Timezone not found for location")

    return local_datetime.replace(tzinfo=ZoneInfo(timezone_name)), timezone_name


def _utc_offset(local_datetime: datetime) -> str:
    offset = local_datetime.strftime("%z")

    return f"{offset[:3]}:{offset[3:]}"


def compute_zodiac_chart(
    birth_datetime: Annotated[
        datetime,
        Field(
            description=(
                "Local birth date and time without a UTC offset."
            )
        ),
    ],
    city: Annotated[
        str,
        Field(description="City of the birthplace.", min_length=1),
    ],
    country: Annotated[
        str,
        Field(description="Country of the birthplace.", min_length=1),
    ],
) -> dict[str, object]:
    """Compute a tropical zodiac chart with Placidus houses.

    Args:
        birth_datetime: Local birth date and time without a UTC offset.
        city: City of the birthplace.
        country: Country of the birthplace.

    Returns:
        Planetary placements, house cusps, Ascendant, and Midheaven.

    Raises:
        ValueError: If the birth date and time includes a UTC offset or the
            location or timezone cannot be resolved.
    """

    if birth_datetime.utcoffset() is not None:
        raise ValueError("birth_datetime must be a local time without a UTC offset")

    latitude, longitude = get_coordinates(city, country)
    local_datetime, timezone_name = _localize_datetime(
        birth_datetime,
        latitude,
        longitude,
    )
    utc_datetime = local_datetime.astimezone(timezone.utc)
    utc_hour = (
        utc_datetime.hour
        + utc_datetime.minute / 60
        + utc_datetime.second / 3600
        + utc_datetime.microsecond / 3_600_000_000
    )
    julian_day = swe.julday(
        utc_datetime.year,
        utc_datetime.month,
        utc_datetime.day,
        utc_hour,
        swe.GREG_CAL,
    )
    planetary_positions = {
        name: _planetary_position(julian_day, planet_id)
        for name, planet_id in ZODIAC_PLANETS.items()
    }
    house_cusps, angles = swe.houses(
        julian_day,
        latitude,
        longitude,
        b"P",
    )

    return {
        "datetime_local": local_datetime.isoformat(),
        "datetime_utc": utc_datetime.isoformat(),
        "julian_day": julian_day,
        "zodiac": "tropical",
        "house_system": "Placidus",
        "location": {
            "city": city,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone_name,
            "utc_offset": _utc_offset(local_datetime),
        },
        "planets": planetary_positions,
        "houses": [
            {"house": house_number, **_zodiac_position(cusp)}
            for house_number, cusp in enumerate(house_cusps, start=1)
        ],
        "angles": {
            "Ascendant": _zodiac_position(angles[0]),
            "Midheaven": _zodiac_position(angles[1]),
        },
    }


async def lyrics_search(
    query: Annotated[
        str,
        Field(description="Query to search for relevant lyrics text chunks."),
    ],
    query_language: Annotated[
        Literal[
            "English",
            "Spanish",
            "French",
        ],
        Field(
            description="Language of the input query and matching lyrics chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Lyrics sources.

    Args:
        query: Query to search for relevant lyrics text chunks.
        query_language: Language of the input query and matching lyrics chunks.
    """

    search_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.language",
                match=models.MatchValue(value=query_language),
            )
        ],
    )

    return await hybrid_search(
        query=query,
        collection_name="lyrics",
        search_filter=search_filter,
    )


async def search_by_chunk_metadata_filters(
    ctx: RunContext,
    query: Annotated[
        str,
        Field(description="Query to search for relevant text chunks."),
    ],
    metadata_filters: Annotated[
        list[ChunkMetadataFilter],
        Field(
            description="Chunk metadata key and value filters to narrow the search by.",
            min_length=1,
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search filtered by chunk metadata values.

    Args:
        query: Query to search for relevant text chunks.
        metadata_filters: Chunk metadata key and value filters to narrow
            the search by.
    """

    deps = ctx.deps
    assert deps is not None

    search_filter = models.Filter(
        must=[
            models.FieldCondition(
                key=f"metadata.{metadata_filter.key}",
                match=models.MatchValue(value=metadata_filter.value),
            )
            for metadata_filter in metadata_filters
        ],
    )

    return await hybrid_search(
        query=query,
        collection_name=deps.collection_name,  # type: ignore
        search_filter=search_filter,
    )


async def get_neighboring_text_chunks(
    ctx: RunContext,
    chunk_id: Annotated[
        str,
        Field(description="chunk_id value of the center text chunk."),
    ],
    before: Annotated[
        int,
        Field(description="Number of previous chunks to retrieve.", ge=0, le=5),
    ] = 1,
    after: Annotated[
        int,
        Field(description="Number of next chunks to retrieve.", ge=0, le=5),
    ] = 1,
) -> list[TextChunk]:
    """Retrieve neighboring text chunks around a center chunk.

    Args:
        chunk_id: chunk_id value of the center text chunk.
        before: Number of previous chunks to retrieve.
        after: Number of next chunks to retrieve.
    """

    deps = ctx.deps
    assert deps is not None

    chunks = await retriever.get_neighboring_text_chunks(
        collection_name=deps.collection_name,  # type: ignore
        chunk_id=chunk_id,
        before=before,
        after=after,
    )

    return [TextChunk(**chunk.model_dump()) for chunk in chunks]


philosophy_search_tool = Tool(
    function=philosophy_search,
    description=(
        "Run a hybrid search across Philosophy sources using a Spanish query."
    ),
    docstring_format="google",
    require_parameter_descriptions=True,
)

satc_search_tool = Tool(
    function=satc_search,
    description=(
        "Run a hybrid search across Sex and the City scripts using an English query."
    ),
    docstring_format="google",
    require_parameter_descriptions=True,
)

astrology_search_tool = Tool(
    function=astrology_search,
    description="Run a hybrid search across Astrology sources.",
    docstring_format="google",
    require_parameter_descriptions=True,
)

astro_weekly_general_tendencies_tool = Tool(
    function=get_astro_weekly_general_tendencies,
    description="Return The Weekly Horoscope general tendencies.",
    docstring_format="google",
    require_parameter_descriptions=True,
)

astro_weekly_horoscope_by_sign_tool = Tool(
    function=get_astro_weekly_horoscope_by_sign,
    description="Return The Weekly Horoscope for a zodiac sign.",
    docstring_format="google",
    require_parameter_descriptions=True,
)

compute_zodiac_chart_tool = Tool(
    function=compute_zodiac_chart,
    description=(
        "Compute a tropical zodiac chart with planetary placements, Placidus "
        "houses, Ascendant, and Midheaven."
    ),
    docstring_format="google",
    require_parameter_descriptions=True,
)

lyrics_search_tool = Tool(
    function=lyrics_search,
    description="Run a hybrid search across Lyrics sources by language.",
    docstring_format="google",
    require_parameter_descriptions=True,
)

search_by_chunk_metadata_filters_tool = Tool(
    function=search_by_chunk_metadata_filters,
    description="Run a hybrid search filtered by chunk metadata values.",
    docstring_format="google",
    require_parameter_descriptions=True,
)

get_neighboring_text_chunks_tool = Tool(
    function=get_neighboring_text_chunks,
    description="Retrieve neighboring text chunks around a center chunk.",
    docstring_format="google",
    require_parameter_descriptions=True,
)

store_relevant_chunk_ids_tool = Tool(
    function=store_relevant_chunk_ids,
    description="Store relevant chunk IDs for the current retrieval request.",
    docstring_format="google",
    require_parameter_descriptions=True,
    max_retries=3,
)

count_flux_tokens_tool = Tool(
    function=count_flux_tokens,
    description="Count the FLUX T5 tokens in a string.",
    docstring_format="google",
    require_parameter_descriptions=True,
)
