from typing import Any

from multi_agents.graph import Node

from por.llm_agents import AstrologyPlacementsExtractor
from por.multi_agent.console import render_node_banner, render_node_detail
from por.multi_agent.schema import StateSchema


async def run(state: StateSchema) -> dict[str, Any]:
    render_node_banner("astrology_placements_extractor")

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    ape = AstrologyPlacementsExtractor()
    ape_output = await ape.generate(
        user_prompt=(f"**Question**: {audio_transcription}"),
    )

    render_node_detail("sun", ape_output.sun or "UNKNOWN")
    render_node_detail("moon", ape_output.moon or "UNKNOWN")
    render_node_detail("rising", ape_output.rising or "UNKNOWN")

    return {
        "astrology_placements": ape_output,
    }


astrology_placements_extractor = Node(
    name="astrology_placements_extractor",
    run=run,
)
