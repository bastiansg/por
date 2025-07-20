from typing import Any
from gpiozero import Button
from functools import lru_cache
from common.logger import get_logger

from pydantic_ai.tools import RunContext
from pydantic_ai.mcp import CallToolFunc, ToolResult

from rage.retriever import Retriever
from sensehat_dsp.display import Display


logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    return Retriever()


@lru_cache(maxsize=1)
def get_sensehat_dsp() -> Display:
    return Display()


@lru_cache(maxsize=1)
def get_button() -> Button:
    return Button(
        pin=16,
        hold_time=0.001,
        bounce_time=0.001,
    )


async def process_tool_call(
    ctx: RunContext[int],
    call_tool: CallToolFunc,
    tool_name: str,
    args: dict[str, Any],
) -> ToolResult:
    call_result = await call_tool(
        tool_name,
        args,
        metadata={"deps": ctx.deps},
    )

    logger.info(
        {
            "tool": tool_name,
            "args": args,
            "result": call_result,
        }
    )

    return call_result
