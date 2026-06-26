import json

from async_lru import alru_cache
from typing import Any, AsyncIterator

from pydantic_ai.messages import AgentStreamEvent
from pydantic_ai import RunContext, FunctionToolCallEvent, ToolDefinition


from por.loaders import AstroWeeklyLoader
from por.multi_agent.console import render_node_detail, render_tool_call


TOOL_CALL_LIMIT = 5


async def hide_tools_after_limit(
    ctx: RunContext,
    tool_defs: list[ToolDefinition],
) -> list[ToolDefinition] | None:
    if ctx.usage.tool_calls >= TOOL_CALL_LIMIT:
        render_node_detail("tool_call_limit_reached", TOOL_CALL_LIMIT)
        return None

    return tool_defs


async def tool_logging_handler(
    run_context: RunContext[Any],
    stream: AsyncIterator[AgentStreamEvent],
) -> None:
    async for event in stream:
        if isinstance(event, FunctionToolCallEvent):
            render_tool_call(
                tool_name=event.part.tool_name,
                parameters=json.loads(event.part.args),  # type: ignore
            )


@alru_cache()
async def get_astro_weekly_data() -> dict:
    loader = AstroWeeklyLoader()
    docs = await loader.load()

    return {doc.metadata["sign_id"]: doc for doc in docs}
