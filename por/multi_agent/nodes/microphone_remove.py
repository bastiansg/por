from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import MicrophoneRemover
from por.multi_agent.schema import StateSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing microphone_remover...")

    image_description = state.image_description
    assert image_description is not None

    microphone_remover = MicrophoneRemover()
    microphone_removed_output = await microphone_remover.generate(
        user_prompt="Remove microphone, cable, and held-object references from this image description.",
        agent_deps=image_description,
    )

    return {
        "image_description": microphone_removed_output,
    }


microphone_remove = Node(
    name="microphone_remover",
    run=run,
)
