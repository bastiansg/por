from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from pydantic_ai import ToolOutput, Tool

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import retrieval_assistant

from ..utils import hide_tools_after_limit, tool_logging_handler


class RetrievalAssistantDeps(BaseModel):
    search_tool: StrictStr
    search_languages: list[LanguageName]


class RetrievalAssistantOutput(BaseModel):
    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of relevant `chunk_id` values.",
        min_length=1,
    )


class RetrievalAssistant(
    LLMAgent[RetrievalAssistantDeps, RetrievalAssistantOutput]
):
    def __init__(
        self,
        conf_path=f"{retrieval_assistant.__path__[0]}/retrieval-assistant.yml",
        max_concurrency: int = 10,
        retries: int = 3,
        tools: list[Tool] = [],
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=RetrievalAssistantDeps,
            output_type=ToolOutput(RetrievalAssistantOutput),  # type: ignore
            max_concurrency=max_concurrency,
            retries=retries,
            prepare_tools=hide_tools_after_limit,
            tools=tools,
            event_stream_handler=tool_logging_handler,  # type: ignore
        )
