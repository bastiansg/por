import random

from typing import Any
from langgraph.runtime import get_runtime

from multi_agents.graph import Node

from rich.console import Console
from por.multi_agent.schema import StateSchema, ContextSchema


console = Console()


async def run(state: StateSchema) -> dict[str, Any]:
    console.log("runing random_selector...")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    return {
        "selected_fc_message": random.choice(
            runtime_context.fc_messages
        ).message,
        "selected_dc_poem": random.choice(runtime_context.dc_poems).poem,
        "lucky_number": random.randint(1, 22),
    }


random_selector = Node(
    name="random_selector",
    run=run,
)
