from typing import Any
from uuid import uuid4

from multi_agents.graph import Node

from por.llm_agents import (
    RetrievalAssistant,
    RetrievalAssistantDeps,
    SATCAdvisor,
    SATCAdvisorDeps,
)
from por.llm_agents.tools import (
    get_neighboring_text_chunks_tool,
    get_relevant_chunk_ids,
    satc_search_tool,
    search_by_chunk_metadata_filters_tool,
)
from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import StateSchema

from .utils import get_relevant_text_chunks

COLLECTION_NAME = "satc"


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

    render_node_banner("satc_advisor")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            satc_search_tool,
            search_by_chunk_metadata_filters_tool,  # type: ignore
            get_neighboring_text_chunks_tool,  # type: ignore
        ]
    )

    retrieval_request_id = uuid4().hex
    question_text = f"**Question**: {audio_transcription}"
    await ra.generate(
        user_prompt=question_text,
        agent_deps=RetrievalAssistantDeps(
            request_id=retrieval_request_id,
            search_tool="satc_search",
            search_languages=["English"],  # type: ignore
            collection_name=COLLECTION_NAME,
        ),
    )

    ra_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=await get_relevant_chunk_ids(retrieval_request_id),
        collection_name=COLLECTION_NAME,
    )

    user_prompt = (
        f"{question_text}\n\n"
        f"**Psychological Profile**: {psychological_profile}\n\n"
        f"**Text Chunks**: {ra_text_chunks}"
    )

    sa = SATCAdvisor()
    satc_output = await sa.generate(
        user_prompt=user_prompt,
        agent_deps=SATCAdvisorDeps(
            output_language=detected_language,
        ),
    )

    return {
        "satc_advice": satc_output.answer,
        "satc_text_chunks": ra_text_chunks,
    }


satc_advisor = Node(
    name="satc_advisor",
    run=run,
)
