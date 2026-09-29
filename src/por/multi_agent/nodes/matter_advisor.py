from typing import Any

from multi_agents.graph import Node

from por.llm_agents import (
    MatterAdvisor,
    MatterAdvisorDeps,
)
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

    advisor = MatterAdvisor()
    advisor_output = await advisor.generate(
        user_prompt=(
            f"**Question**: {audio_transcription}\n\n"
            f"**Psychological Profile**: {psychological_profile}"
        ),
        agent_deps=MatterAdvisorDeps(
            search_languages=["English", "Spanish", "French"],  # type: ignore
            collection_name=COLLECTION_NAME,
            output_language=detected_language,
        ),
    )
    text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=advisor_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    return {
        "matter_advise": advisor_output.answer,
        "matter_text_chunks": text_chunks,
        "matter_web_results": advisor_output.relevant_web_results,
    }


matter_advisor = Node(
    name="matter_advisor",
    run=run,
)
