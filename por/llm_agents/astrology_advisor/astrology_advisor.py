from pydantic_ai import NativeOutput

from pydantic import BaseModel, Field, StrictStr
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import astrology_advisor
from por.meta.schema import TextChunk, AstrologyPlacements, PsychologicalProfile


class AstrologyAdvisorDeps(BaseModel):
    astrology_placements: AstrologyPlacements
    psychological_profile: PsychologicalProfile
    text_chunks: list[TextChunk]
    output_language: LanguageName


class AstrologyAdvisorOutput(BaseModel):
    answer: StrictStr = Field(
        description="Your intuitive, symbolic, and emotionally clarifying message.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of unique `chunk_id` values that influenced your answer.",
        min_length=1,
    )


class AstrologyAdvisor(LLMAgent[AstrologyAdvisorDeps, AstrologyAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{astrology_advisor.__path__[0]}/astrology-advisor.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=AstrologyAdvisorDeps,
            output_type=NativeOutput(AstrologyAdvisorOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
