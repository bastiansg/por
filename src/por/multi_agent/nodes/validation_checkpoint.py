from typing import Any

from multi_agents.graph import Node

from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import StateSchema


async def run(state: StateSchema) -> dict[str, Any]:
    render_node_banner("validation_checkpoint")

    if state.message_accepted:
        return {
            "message_accepted": True,
            "rejection_reason": None,
        }

    return {}


validation_checkpoint = Node(
    name="validation_checkpoint",
    run=run,
)
