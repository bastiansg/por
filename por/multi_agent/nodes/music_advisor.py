import re

from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents.tools import _get_text_chunk
from por.llm_agents import MusicAdvisor, MusicAdvisorDeps
from por.multi_agent.schema import StateSchema


logger = get_logger(__name__)


def clean_music_advice(music_advice: str) -> str:
    return re.sub(r"\s+", " ", music_advice).strip()


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing music_advisor...")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    music_advisor = MusicAdvisor()
    async with music_advisor.agent:
        music_advisor_output = await music_advisor.generate(
            user_prompt="Provide your pure, poetic, emotionally saturated lyrics.",
            agent_deps=MusicAdvisorDeps(
                psychological_profile=psychological_profile,
                question=audio_transcription,
                output_language=detected_language,
            ),
        )

    relevant_chunk = _get_text_chunk(
        chunk_id=music_advisor_output.relevant_chunk_id
    )

    # FIXME: Do not use if / else!
    if relevant_chunk is not None:
        payload = relevant_chunk.payload
        assert payload is not None

        selected_song = {
            "title": payload["metadata"].get("title"),
            "artist": payload["metadata"].get("artist"),
            "lyrics": payload["page_content"],
        }

    else:
        selected_song = {
            "title": "Unknown",
            "artist": "Unknown",
            "lyrics": "Unknown",
        }

    return {
        "music_advice": clean_music_advice(
            music_advice=music_advisor_output.music_advice
        ),
        "selected_song": selected_song,
    }


music_advisor = Node(
    name="music_advisor",
    run=run,
)
