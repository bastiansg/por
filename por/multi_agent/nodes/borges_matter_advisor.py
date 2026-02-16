from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.db.qdrant import get_text_chunk
from por.multi_agent.schema import StateSchema
from por.llm_agents import BorgesMatterAdvisor, BorgesMatterAdvisorDeps


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing borges_matter_advisor...")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    bma = BorgesMatterAdvisor()
    ma_output = await bma.generate(
        user_prompt="Provide a profound, poetic, and metaphysical piece of advice about matter.",
        agent_deps=BorgesMatterAdvisorDeps(
            psychological_profile=psychological_profile,
            question=audio_transcription,
            output_language=detected_language,
        ),
    )

    relevant_chunk_ids = ma_output.relevant_chunk_ids
    logger.info(f"relevant_chunk_ids: {len(relevant_chunk_ids)}")
    chunk_records = [
        await get_text_chunk(
            collection_name="matter",
            key="chunk_id",
            value=chunk_id,
        )
        for chunk_id in relevant_chunk_ids
    ]

    borges_matter_text_chunks = [
        chunk_record.payload["page_content"]
        for chunk_record in chunk_records
        if chunk_record is not None and chunk_record.payload is not None
    ]

    return {
        "borges_matter_advise": ma_output.borges_matter_advise,
        "borges_matter_text_chunks": borges_matter_text_chunks,
    }


borges_matter_advisor = Node(
    name="borges_matter_advisor",
    run=run,
)
