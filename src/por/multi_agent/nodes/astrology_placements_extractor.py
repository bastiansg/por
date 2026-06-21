from typing import Any

from multi_agents.graph import Node

from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import StateSchema
from por.llm_agents import AstrologyPlacementsExtractor


async def run(state: StateSchema) -> dict[str, Any]:
    render_node_banner("astrology_placements_extractor")

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
