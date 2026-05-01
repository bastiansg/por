from typing import Any

from multi_agents.graph import Node
from rich.console import Console

from por.llm_agents import LanguageDetector
from por.multi_agent.schema import StateSchema


console = Console()


async def run(state: StateSchema) -> dict[str, Any]:
    console.log("runing language_detector...")

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    ld = LanguageDetector()
    ld_output = await ld.generate(
        user_prompt=f"Identify the primary language of the following user query: {audio_transcription}",
    )

    detected_language = ld_output.language
    assert detected_language is not None

    detected_language = detected_language.name
    console.log(f"detected_language: {detected_language}")

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
