from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema
from por.llm_agents.tools import borges_search_tool, get_text_chunk_tool
from por.llm_agents import (
    RetrievalAssistant,
    RetrievalAssistantDeps,
    BorgesMatterAdvisor,
    BorgesMatterAdvisorDeps,
)

from .utils import get_text_chunks


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing borges_matter_advisor...")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            borges_search_tool,
            get_text_chunk_tool,
        ]
    )

    ra_output = await ra.generate(
        user_prompt=f"**Question**: {audio_transcription}",
        agent_deps=RetrievalAssistantDeps(
            search_tool="borges_search",
            search_languages=["Spanish"],  # type: ignore
        ),
    )

    ra_text_chunks = await get_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name="borges",
    )

    bma = BorgesMatterAdvisor()
    ma_output = await bma.generate(
        user_prompt="Provide your profound, poetic, and metaphysical message.",
        agent_deps=BorgesMatterAdvisorDeps(
            psychological_profile=psychological_profile,
            question=audio_transcription,
            text_chunks=ra_text_chunks,
            output_language=detected_language,
        ),
    )

    ma_text_chunks = await get_text_chunks(
        relevant_chunk_ids=ma_output.relevant_chunk_ids,
        collection_name="borges",
    )

    return {
        "borges_matter_advise": ma_output.answer,
        "borges_matter_text_chunks": ma_text_chunks,
    }


borges_matter_advisor = Node(
    name="borges_matter_advisor",
    run=run,
)
