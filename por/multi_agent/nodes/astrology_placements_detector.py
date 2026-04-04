from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import AstrologyPlacementsDetector
from por.multi_agent.schema import StateSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing astrology_placements_detector...")

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    astrology_placements_detector_agent = AstrologyPlacementsDetector()
    astrology_placements_output = (
        await astrology_placements_detector_agent.generate(
            user_prompt=f"**User Query**: {audio_transcription}",
        )
    )

    return {
        "astrology_placements": astrology_placements_output,
    }


astrology_placements_detector = Node(
    name="astrology_placements_detector",
    run=run,
)
