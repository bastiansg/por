from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, StrictBool, StrictStr
from pydantic_ai import Agent, RunContext, Tool, ToolOutput
from pydantic_ai.capabilities import PrepareTools, ProcessEventStream
from pydantic_ai.models.openai import OpenAIChatModelSettings
from pydantic_extra_types.language_code import LanguageName

from ..tools import store_relevant_chunk_ids_tool
from ..utils import hide_tools_after_limit, tool_logging_handler


class RetrievalAssistantDeps(BaseModel):
    request_id: StrictStr
    search_tool: StrictStr
    search_languages: list[LanguageName]
    collection_name: StrictStr


class RetrievalAssistantOutput(BaseModel):
    retrieval_stored: StrictBool = Field(
        description="Whether the relevant chunk IDs were stored successfully.",
    )


def get_agent(
    tools: list[Tool] = [],
) -> Agent[
    RetrievalAssistantDeps,
    RetrievalAssistantOutput,
]:

    agent = Agent(  # type: ignore
        name="retrieval-assistant",
        model="openai-chat:gpt-5.6-luna",
        model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
        system_prompt=LLMAgent.read_file(
            file_path=str(Path(__file__).with_name("system-prompt.md"))
        ),
        deps_type=RetrievalAssistantDeps,
        output_type=ToolOutput(RetrievalAssistantOutput),
        retries=3,
        tools=[*tools, store_relevant_chunk_ids_tool],
        capabilities=[
            PrepareTools(hide_tools_after_limit),  # type: ignore
            ProcessEventStream(tool_logging_handler),  # type: ignore
        ],
    )

    @agent.system_prompt  # type: ignore
    async def get_system_prompt(ctx: RunContext[RetrievalAssistantDeps]) -> str:
        system_prompt = LLMAgent.read_file(
            file_path=str(Path(__file__).with_name("system-prompt.md"))
        )

        return system_prompt.format(**ctx.deps.model_dump())

    return agent  # type: ignore


class RetrievalAssistant(
    LLMAgent[RetrievalAssistantDeps, RetrievalAssistantOutput]
):
    def __init__(self, max_concurrency: int = 10, tools: list[Tool] = []):
        super().__init__(
            agent=get_agent(tools=tools),
            max_concurrency=max_concurrency,
        )
