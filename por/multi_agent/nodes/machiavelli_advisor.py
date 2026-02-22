from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema
from por.llm_agents.tools import machiavelli_search_tool, get_text_chunk_tool
from por.llm_agents import (
    MachiavelliAdvisor,
    MachiavelliAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import get_text_chunks


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("running machiavellian_advisor...")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            machiavelli_search_tool,
            get_text_chunk_tool,
        ]
    )

    ra_output = await ra.generate(
        user_prompt=f"**Question**: {audio_transcription}",
        agent_deps=RetrievalAssistantDeps(
            search_tool="machiavelli_search",
            search_languages=["Spanish"],  # type: ignore
        ),
    )

    ra_text_chunks = await get_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name="machiavelli",
    )

    ma = MachiavelliAdvisor()
    ma_output = await ma.generate(
        user_prompt="Offer ruthless, strategic advice focusing on power and leverage.",
        agent_deps=MachiavelliAdvisorDeps(
            psychological_profile=psychological_profile,
            question=audio_transcription,
            text_chunks=ra_text_chunks,
            output_language=detected_language,
        ),
    )

    ma_text_chunks = await get_text_chunks(
        relevant_chunk_ids=ma_output.relevant_chunk_ids,
        collection_name="machiavelli",
    )

    return {
        "machiavelli_advice": ma_output.answer,
        "machiavelli_text_chunks": ma_text_chunks,
    }


machiavelli_advisor = Node(
    name="machiavelli_advisor",
    run=run,
)
