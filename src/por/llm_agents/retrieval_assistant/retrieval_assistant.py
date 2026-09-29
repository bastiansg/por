from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, StrictBool, StrictStr
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.capabilities import PrepareTools, ProcessEventStream
from pydantic_ai.models.openai import OpenAIResponsesModelSettings
from pydantic_extra_types.language_code import LanguageName

from ..tools import (
    get_neighboring_text_chunks_tool,
    matter_search_tool,
    search_by_chunk_metadata_filters_tool,
    store_relevant_chunk_ids_tool,
)
from ..utils import hide_tools_after_limit, tool_logging_handler


class RetrievalAssistantDeps(BaseModel):
    request_id: StrictStr
    search_languages: list[LanguageName]
    collection_name: StrictStr


class RetrievalAssistantOutput(BaseModel):
    retrieval_stored: StrictBool = Field(
        description="Whether the relevant chunk IDs were stored successfully.",
    )


def get_agent() -> Agent[
    RetrievalAssistantDeps,
    RetrievalAssistantOutput,
]:

    agent = Agent(
        name="retrieval-assistant",
        model="openai:gpt-5.6-luna",
        model_settings=OpenAIResponsesModelSettings(openai_reasoning_effort="low"),
        deps_type=RetrievalAssistantDeps,
        output_type=ToolOutput(RetrievalAssistantOutput),
        retries=3,
        tools=[
            matter_search_tool,
            search_by_chunk_metadata_filters_tool,  # type: ignore
            get_neighboring_text_chunks_tool,  # type: ignore
            store_relevant_chunk_ids_tool,
        ],
        capabilities=[
            PrepareTools(hide_tools_after_limit),
            ProcessEventStream(tool_logging_handler),  # type: ignore
        ],
    )

    @agent.system_prompt
    async def get_system_prompt(ctx: RunContext[RetrievalAssistantDeps]) -> str:
        system_prompt = LLMAgent.read_file(
            file_path=str(Path(__file__).with_name("system-prompt.md"))
        )

        return system_prompt.format(**ctx.deps.model_dump())

    return agent


class RetrievalAssistant(
    LLMAgent[RetrievalAssistantDeps, RetrievalAssistantOutput]
):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(
            agent=get_agent(),
            max_concurrency=max_concurrency,
        )
