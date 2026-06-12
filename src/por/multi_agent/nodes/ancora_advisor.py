from typing import Any

from multi_agents.graph import Node
from rich.console import Console

from por.multi_agent.schema import StateSchema
from por.llm_agents.tools import ancora_search_tool, get_text_chunks_tool
from por.llm_agents import (
    AncoraAdvisor,
    AncoraAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import get_relevant_text_chunks


console = Console()


COLLECTION_NAME = "ancora"


async def run(state: StateSchema) -> dict[str, Any]:
    console.log("running ancora_advisor...")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            ancora_search_tool,
            get_text_chunks_tool,  # type: ignore
        ]
    )

    question_text = f"**Question**: {audio_transcription}"
    ra_output = await ra.generate(
        user_prompt=question_text,
        agent_deps=RetrievalAssistantDeps(
            search_tool="ancora_search",
            search_languages=["English", "Spanish"],  # type: ignore
            collection_name=COLLECTION_NAME,
        ),
    )

    ra_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    aa = AncoraAdvisor()
    ancora_output = await aa.generate(
        user_prompt=question_text,
        agent_deps=AncoraAdvisorDeps(
            psychological_profile=psychological_profile,
            text_chunks=ra_text_chunks,
            output_language=detected_language,
        ),
    )

    ancora_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=ancora_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    return {
        "ancora_advice": ancora_output.answer,
        "ancora_text_chunks": ancora_text_chunks,
    }


ancora_advisor = Node(
    name="ancora_advisor",
    run=run,
)
