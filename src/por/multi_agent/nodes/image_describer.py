import asyncio
from pathlib import Path
from typing import Any

from langgraph.runtime import get_runtime
from multi_agents.graph import Node
from pydantic_ai import BinaryContent

from por.llm_agents import (
    MicrophoneRemover,
    PBFImageDescriber,
    PBFImageDescriberDeps,
)
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
        agent_deps=PBFImageDescriberDeps(
            caption_header=runtime_context.caption_header,
            t5_tokenizer_name=runtime_context.t5_tokenizer_name,
            flux_max_tokens=runtime_context.flux_max_tokens,
        ),
        user_content=BinaryContent(
            data=image_data,
            media_type=f"image/{runtime_context.input_image_extension}",
        ),
    )

    microphone_remover = MicrophoneRemover()
    microphone_removed_output = await microphone_remover.generate(
        user_prompt=(
            "Remove microphone, cable, and held-object references from this "
            "image description."
            f"\n\n**Image Description**: {image_describer_output}"
        ),
    )

    return {
        "image_description": microphone_removed_output,
    }


image_describer = Node(
    name="image_describer",
    run=run,
)
