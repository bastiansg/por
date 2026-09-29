from typing import Any
from uuid import uuid4

from multi_agents.graph import Node

from por.llm_agents import (
    MatterAdvisor,
    MatterAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)
from por.llm_agents.tools import get_relevant_chunk_ids
from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import StateSchema

from .utils import get_relevant_text_chunks

COLLECTION_NAME = "matter"


async def run(state: StateSchema) -> dict[str, Any]:
    render_node_banner("matter_advisor")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription
    detected_language = state.detected_language

    assert psychological_profile is not None
    assert audio_transcription is not None
    assert detected_language is not None

    retrieval_assistant = RetrievalAssistant()
    retrieval_request_id = uuid4().hex
    await retrieval_assistant.generate(
        user_prompt=f"**Question**: {audio_transcription}",
        agent_deps=RetrievalAssistantDeps(
            request_id=retrieval_request_id,
            search_languages=["English", "Spanish", "French"],  # type: ignore
            collection_name=COLLECTION_NAME,
        ),
    )

    text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=await get_relevant_chunk_ids(retrieval_request_id),
        collection_name=COLLECTION_NAME,
    )
    advisor = MatterAdvisor()
    advisor_output = await advisor.generate(
        user_prompt=(
            f"**Question**: {audio_transcription}\n\n"
            f"**Psychological Profile**: {psychological_profile}\n\n"
            f"**Text Chunks**: {text_chunks}"
        ),
        agent_deps=MatterAdvisorDeps(output_language=detected_language),
    )

    return {
        "matter_advise": advisor_output.answer,
        "matter_text_chunks": text_chunks,
    }


matter_advisor = Node(
    name="matter_advisor",
    run=run,
)
