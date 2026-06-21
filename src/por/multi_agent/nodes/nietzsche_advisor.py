from typing import Any

from multi_agents.graph import Node

from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import StateSchema
from por.llm_agents.tools import philosophy_search_tool, get_text_chunks_tool
from por.llm_agents import (
    NietzscheAdvisor,
    NietzscheAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import get_relevant_text_chunks


COLLECTION_NAME = "philosophy"


async def run(state: StateSchema) -> dict[str, Any]:
    astrology_placements = state.astrology_placements
    assert astrology_placements is not None

    if any(
        [
            astrology_placements.sun is not None,
            astrology_placements.rising is not None,
            astrology_placements.moon is not None,
        ]
    ):
        return {}

    render_node_banner("nietzsche_advisor")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            philosophy_search_tool,
            get_text_chunks_tool,  # type: ignore
        ]
    )

    question_text = f"**Question**: {audio_transcription}"
    ra_output = await ra.generate(
        user_prompt=f"**Question**: {audio_transcription}",
        agent_deps=RetrievalAssistantDeps(
            search_tool="philosophy_search",
            search_languages=["Spanish"],  # type: ignore
            collection_name=COLLECTION_NAME,
        ),
    )

    ra_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    na = NietzscheAdvisor()
    na_output = await na.generate(
        user_prompt=question_text,
        agent_deps=NietzscheAdvisorDeps(
            psychological_profile=psychological_profile,
            text_chunks=ra_text_chunks,
            output_language=detected_language,
        ),
    )

    na_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=na_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    return {
        "nietzsche_advise": na_output.answer,
        "nietzsche_text_chunks": na_text_chunks,
    }


nietzsche_advisor = Node(
    name="nietzsche_advisor",
    run=run,
)
