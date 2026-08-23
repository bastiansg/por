import asyncio
from pathlib import Path
from typing import Any

from langgraph.runtime import get_runtime
from multi_agents.graph import Node
from pydantic_ai import BinaryContent

from por.llm_agents import PBFImageDescriber
from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import ContextSchema, StateSchema


async def run(state: StateSchema) -> dict[str, Any]:
    render_node_banner("image_describer")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    image_path = state.image_path
    assert image_path is not None

    image_describer_agent = PBFImageDescriber()
    image_data = await asyncio.to_thread(Path(image_path).read_bytes)
    image_describer_output = await image_describer_agent.generate(
        user_prompt="Analyze the provided image.",
        user_content=BinaryContent(
            data=image_data,
            media_type=f"image/{runtime_context.image_extension}",
        ),
    )

    return {
        "image_description": image_describer_output,
    }


image_describer = Node(
    name="image_describer",
    run=run,
)
