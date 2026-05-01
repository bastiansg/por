from typing import Any

from multi_agents.graph import Node
from rich.console import Console

from por.multi_agent.schema import StateSchema


console = Console()


async def run(state: StateSchema) -> dict[str, Any]:
    console.log("running validation_checkpoint...")

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
