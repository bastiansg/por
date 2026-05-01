from typing import Any
from langgraph.runtime import get_runtime

from pydantic_ai import BinaryContent

from multi_agents.graph import Node
from rich.console import Console

from por.llm_agents import ImageDescriber, MicrophoneRemover
from por.multi_agent.schema import StateSchema, ContextSchema


console = Console()


async def run(state: StateSchema) -> dict[str, Any]:
    console.log("runing image_describer...")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    image_path = state.image_path
    assert image_path is not None

    image_describer_agent = ImageDescriber()
    with open(image_path, "rb") as image_file:
        image_describer_output = await image_describer_agent.generate(
            user_prompt="Analyze primary subjects present in the provided image and provide a detailed physical and clothing description.",
            user_content=BinaryContent(
                data=image_file.read(),
                media_type=f"image/{runtime_context.image_extension}",
            ),
        )

    microphone_remover = MicrophoneRemover()
    microphone_removed_output = await microphone_remover.generate(
        user_prompt="Remove microphone, cable, and held-object references from this image description.",
        agent_deps=image_describer_output,
    )

    return {
        "image_description": microphone_removed_output,
    }


image_describer = Node(
    name="image_describer",
    run=run,
)
