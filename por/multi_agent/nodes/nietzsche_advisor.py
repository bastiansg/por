from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema
from por.llm_agents.tools import nietzsche_search_tool, get_text_chunk_tool
from por.llm_agents import (
    NietzscheAdvisor,
    NietzscheAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import get_text_chunks


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing nietzsche_advisor...")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            nietzsche_search_tool,
            get_text_chunk_tool,
        ]
    )

    ra_output = await ra.generate(
        user_prompt=f"**Question**: {audio_transcription}",
        agent_deps=RetrievalAssistantDeps(
            search_tool="nietzsche_search",
            search_languages=["Spanish"],  # type: ignore
        ),
    )

    ra_text_chunks = await get_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name="nietzsche",
    )

    na = NietzscheAdvisor()
    na_output = await na.generate(
        user_prompt="Deliver your piercing, symbolic, and transformative message.",
        agent_deps=NietzscheAdvisorDeps(
            psychological_profile=psychological_profile,
            question=audio_transcription,
            text_chunks=ra_text_chunks,
            output_language=detected_language,
        ),
    )

    na_text_chunks = await get_text_chunks(
        relevant_chunk_ids=na_output.relevant_chunk_ids,
        collection_name="nietzsche",
    )

    return {
        "nietzsche_advise": na_output.answer,
        "nietzsche_text_chunks": na_text_chunks,
    }


nietzsche_advisor = Node(
    name="nietzsche_advisor",
    run=run,
)
