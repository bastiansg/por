from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.db.qdrant import get_text_chunk
from por.multi_agent.schema import StateSchema
from por.llm_agents import NietzscheAdvisor, NietzscheAdvisorDeps


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing nietzsche_advisor...")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    nietzsche_advisor = NietzscheAdvisor()
    async with nietzsche_advisor.agent:
        nietzsche_advisor_output = await nietzsche_advisor.generate(
            user_prompt="Deliver piercing, symbolic, and transformative insight in the style of Nietzsche.",
            agent_deps=NietzscheAdvisorDeps(
                psychological_profile=psychological_profile,
                question=audio_transcription,
                output_language=detected_language,
            ),
        )

    relevant_chunk_ids = nietzsche_advisor_output.relevant_chunk_ids
    logger.info(f"relevant_chunk_ids: {len(relevant_chunk_ids)}")
    chunk_records = [
        await get_text_chunk(
            collection_name="nietzsche",
            key="chunk_id",
            value=chunk_id,
        )
        for chunk_id in relevant_chunk_ids
    ]

    nietzsche_text_chunks = [
        chunk_record.payload["page_content"]
        for chunk_record in chunk_records
        if chunk_record is not None and chunk_record.payload is not None
    ]

    return {
        "nietzsche_advise": nietzsche_advisor_output.nietzsche_advise,
        "nietzsche_text_chunks": nietzsche_text_chunks,
    }


nietzsche_advisor = Node(
    name="nietzsche_advisor",
    run=run,
)
