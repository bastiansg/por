from pydantic_ai import ToolOutput

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import satc_advisor

from ..tools import satc_search_tool, get_text_chunk_tool
from ..utils import tool_logging_handler, hide_tools_after_limit


class SATCAdvisorDeps(BaseModel):
    question: StrictStr
    output_language: LanguageName


class SATCAdvisorOutput(BaseModel):
    satc_advice: StrictStr = Field(
        description="Advice written in Carrie Bradshaw's voice, as if speaking to a close friend at a restaurant.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of `chunk_id` values used to generate the advice.",
        min_length=1,
    )


class SATCAdvisor(LLMAgent[SATCAdvisorDeps, SATCAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{satc_advisor.__path__[0]}/satc-advisor.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=SATCAdvisorDeps,
            output_type=ToolOutput(SATCAdvisorOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
            prepare_tools=hide_tools_after_limit,
            tools=[satc_search_tool, get_text_chunk_tool],
            event_stream_handler=tool_logging_handler,  # type: ignore
        )
