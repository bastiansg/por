from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("running validation_checkpoint...")

    if state.message_accepted or state.exibition_related:
        return {
            "message_accepted": True,
            "rejection_reason": None,
        }

    return {}


validation_checkpoint = Node(
    name="validation_checkpoint",
    run=run,
)
