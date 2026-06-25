from typing import Any

from multi_agents.graph import Node

from por.llm_agents.tools import (
    astrology_search_tool,
    get_neighboring_text_chunks_tool,
    search_by_chunk_metadata_filters_tool,
)
from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import StateSchema
from por.llm_agents import (
    AstrologyAdvisor,
    AstrologyAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import get_relevant_text_chunks


COLLECTION_NAME = "astrology"


async def run(state: StateSchema) -> dict[str, Any]:
    astrology_placements = state.astrology_placements
    assert astrology_placements is not None

    if all(
        [
            astrology_placements.sun is None,
            astrology_placements.rising is None,
            astrology_placements.moon is None,
        ]
    ):
        return {}

    render_node_banner("astrology_advisor")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            astrology_search_tool,
            search_by_chunk_metadata_filters_tool,  # type: ignore
            get_neighboring_text_chunks_tool,  # type: ignore
        ]
    )

    question_text = f"**Question**: {audio_transcription}"
    ra_output = await ra.generate(
        user_prompt=question_text,
        agent_deps=RetrievalAssistantDeps(
            search_tool="astrology_search",
            search_languages=["English", "Spanish"],  # type: ignore
            collection_name=COLLECTION_NAME,
        ),
    )

    ra_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    aa = AstrologyAdvisor()
    astrology_output = await aa.generate(
        user_prompt=question_text,
        agent_deps=AstrologyAdvisorDeps(
            astrology_placements=astrology_placements,
            psychological_profile=psychological_profile,
            text_chunks=ra_text_chunks,
            output_language=detected_language,
        ),
    )

    astrology_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=astrology_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    return {
        "astrology_advice": astrology_output.answer,
        "astrology_text_chunks": astrology_text_chunks,
    }


astrology_advisor = Node(
    name="astrology_advisor",
    run=run,
)
