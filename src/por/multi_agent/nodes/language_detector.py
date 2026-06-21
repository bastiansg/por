from typing import Any

from multi_agents.graph import Node

from por.llm_agents import LanguageDetector
from por.multi_agent.console import render_node_banner, render_node_detail
from por.multi_agent.schema import StateSchema


async def run(state: StateSchema) -> dict[str, Any]:
    render_node_banner("language_detector")

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    ld = LanguageDetector()
    ld_output = await ld.generate(
        user_prompt=f"Identify the primary language of the following user query: {audio_transcription}",
    )

    detected_language = ld_output.language
    assert detected_language is not None

    detected_language = detected_language.name
    render_node_detail("detected_language", detected_language)

    detected_language = (
        detected_language if detected_language is not None else "Spanish"
    )

    return {
        "detected_language": detected_language,
    }


language_detector = Node(
    name="language_detector",
    run=run,
)
