from pathlib import Path

from pydantic_ai import Agent, RunContext, Tool, ToolOutput
from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from ..utils import hide_tools_after_limit, tool_logging_handler


class RetrievalAssistantDeps(BaseModel):
    search_tool: StrictStr
    search_languages: list[LanguageName]
    collection_name: StrictStr


class RetrievalAssistantOutput(BaseModel):
    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of relevant `chunk_id` values.",
        min_length=1,
    )


def get_agent(
    tools: list[Tool] = [],
) -> Agent[
    RetrievalAssistantDeps,
    RetrievalAssistantOutput,
]:

    agent = Agent(  # type: ignore
        # model="gpt-5.4-2026-03-05",
        name="retrieval-assistant",
        model="gpt-5.4-2026-03-05",
        system_prompt=LLMAgent.read_file(
            file_path=str(Path(__file__).with_name("system-prompt.md"))
        ),
        deps_type=RetrievalAssistantDeps,
        output_type=ToolOutput(RetrievalAssistantOutput),
        retries=3,
        tools=tools,
        prepare_tools=hide_tools_after_limit,  # type: ignore
        event_stream_handler=tool_logging_handler,  # type: ignore
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
