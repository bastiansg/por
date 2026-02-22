from pydantic_ai import ToolOutput

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import machiavelli_advisor
from por.meta.schema import TextChunk

from ..psychological_describer.psychological_describer import (
    PsychologicalDescriberOutput,
)


class MachiavelliAdvisorDeps(BaseModel):
    psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    text_chunks: list[TextChunk]
    output_language: LanguageName


class MachiavelliAdvisorOutput(BaseModel):
    answer: StrictStr = Field(
        description="Your ruthless, strategic message focusing on power and leverage.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of unique `chunk_id` values that influenced your answer.",
        min_length=1,
    )


class MachiavelliAdvisor(
    LLMAgent[MachiavelliAdvisorDeps, MachiavelliAdvisorOutput]
):
    def __init__(
        self,
        conf_path=f"{machiavelli_advisor.__path__[0]}/machiavellian-advisor.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=MachiavelliAdvisorDeps,
            output_type=ToolOutput(MachiavelliAdvisorOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
