from pydantic_ai import NativeOutput
from pydantic_ai.models import Model
from pydantic import BaseModel, Field
from typing import Literal

from common.cache import RedisCache
from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import astrology_placements_detector


ZodiacSign = Literal[
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
]


class AstrologyPlacementsDetectorOutput(BaseModel):
    sun: ZodiacSign | None = Field(
        description="The user's astrological sun sign."
    )

    moon: ZodiacSign | None = Field(
        description="The user's astrological moon sign."
    )

    rising: ZodiacSign | None = Field(
        description="The user's astrological rising sign."
    )


class AstrologyPlacementsDetector(
    LLMAgent[None, AstrologyPlacementsDetectorOutput]
):
    def __init__(
        self,
        conf_path: str = f"{astrology_placements_detector.__path__[0]}/astrology-placements-detector.yml",
        model: Model | None = None,
        max_concurrency: int = 10,
        cache: RedisCache | None = None,
        retries: int = 3,
    ):
        super().__init__(
            conf_path=conf_path,
            output_type=NativeOutput(AstrologyPlacementsDetectorOutput),  # type: ignore
            model=model,
            max_concurrency=max_concurrency,
            cache=cache,
            retries=retries,
        )
