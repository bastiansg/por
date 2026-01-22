import json

from typing import Any, AsyncIterator

from pydantic_ai.messages import AgentStreamEvent
from pydantic_ai import RunContext, FunctionToolCallEvent

from common.logger import get_logger


logger = get_logger(__name__)


async def tool_logging_handler(
    run_context: RunContext[Any],
    stream: AsyncIterator[AgentStreamEvent],
) -> None:
    async for event in stream:
        if isinstance(event, FunctionToolCallEvent):
            logger.info(
                {
                    "tool": event.part.tool_name,
                    "args": json.loads(event.part.args),  # type: ignore
                }
            )
