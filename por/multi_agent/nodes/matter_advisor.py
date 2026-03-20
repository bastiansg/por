from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema
from por.llm_agents.tools import (
    matter_search_tool,
    get_text_chunk_tool,
)

from por.llm_agents import (
    MatterAdvisor,
    MatterAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import get_text_chunks


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing matter_advisor...")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            matter_search_tool,  # type: ignore
            get_text_chunk_tool,
        ]
    )

    exibition_related = state.exibition_related
    logger.info(f"exibition_related: {exibition_related}")

    agent_deps = RetrievalAssistantDeps(
        search_tool="matter_search",
        search_languages=["English", "Spanish", "French"],  # type: ignore
        exibition_related=exibition_related,
    )

    ra_output = await ra.generate(
        user_prompt=f"**Question**: {audio_transcription}",
        agent_deps=agent_deps,
    )

    ra_text_chunks = await get_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name="matter",
    )

    ma = MatterAdvisor()
    ma_output = await ma.generate(
        user_prompt="Provide your profound, poetic, and transformative message.",
        agent_deps=MatterAdvisorDeps(
            psychological_profile=psychological_profile,
            question=audio_transcription,
            text_chunks=ra_text_chunks,
            output_language=detected_language,
        ),
    )

    ma_text_chunks = await get_text_chunks(
        relevant_chunk_ids=ma_output.relevant_chunk_ids,
        collection_name="matter",
    )

    return {
        "matter_advise": ma_output.answer,
        "matter_text_chunks": ma_text_chunks,
    }


matter_advisor = Node(
    name="matter_advisor",
    run=run,
)
