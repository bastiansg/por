from pydantic_ai import NativeOutput

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import matter_advisor
from por.meta.schema import TextChunk

from ..psychological_describer.psychological_describer import (
    PsychologicalDescriberOutput,
)


class MatterAdvisorDeps(BaseModel):
    psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    text_chunks: list[TextChunk]
    output_language: LanguageName


class MatterAdvisorOutput(BaseModel):
    answer: StrictStr = Field(
        description="Your profound, poetic, and transformative message.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of unique `chunk_id` values that influenced your answer.",
        min_length=1,
    )


class MatterAdvisor(LLMAgent[MatterAdvisorDeps, MatterAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{matter_advisor.__path__[0]}/matter-advisor.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=MatterAdvisorDeps,
            output_type=NativeOutput(MatterAdvisorOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
