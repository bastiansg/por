from pydantic_ai import ToolOutput

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from por.conf import llm_agents  # type: ignore
from llm_agents.meta.interfaces import LLMAgent

from .psychological_describer import PsychologicalDescriberOutput
from .tools import borges_search_tool, get_text_chunk_tool
from .utils import tool_logging_handler, hide_tools_after_limit


class BorgesMatterAdvisorDeps(BaseModel):
    psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    output_language: LanguageName


class BorgesMatterAdvisorOutput(BaseModel):
    borges_matter_advise: StrictStr = Field(
        description="A profound, poetic, and metaphysical piece of advice from Jorge Luis Borges about matter.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of `chunk_id` values used to generate the advice.",
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
            prepare_tools=hide_tools_after_limit,
            tools=[borges_search_tool, get_text_chunk_tool],
            event_stream_handler=tool_logging_handler,  # type: ignore
        )
