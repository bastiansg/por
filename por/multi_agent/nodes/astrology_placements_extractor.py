from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger


from por.multi_agent.schema import StateSchema
from por.llm_agents import AstrologyPlacementsExtractor


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("running astrology_placements_extractor...")

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    ape = AstrologyPlacementsExtractor()
    ape_output = await ape.generate(
        user_prompt=(f"**Question**: {audio_transcription}"),
    )

    return {
        "astrology_placements": ape_output,
    }


astrology_placements_extractor = Node(
    name="astrology_placements_extractor",
    run=run,
)
