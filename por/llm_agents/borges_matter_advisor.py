from pydantic_ai import ToolOutput

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.conf import llm_agents  # type: ignore
from por.meta.schema import TextChunk

from .psychological_describer import PsychologicalDescriberOutput


class BorgesMatterAdvisorDeps(BaseModel):
    psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    text_chunks: list[TextChunk]
    output_language: LanguageName


class BorgesMatterAdvisorOutput(BaseModel):
    answer: StrictStr = Field(
        description="Your profound, poetic, and metaphysical message.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of unique `chunk_id` values that influenced your advice.",
        min_length=1,
    )


class BorgesMatterAdvisor(
    LLMAgent[BorgesMatterAdvisorDeps, BorgesMatterAdvisorOutput]
):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/borges-matter-advisor.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=BorgesMatterAdvisorDeps,
            output_type=ToolOutput(BorgesMatterAdvisorOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
