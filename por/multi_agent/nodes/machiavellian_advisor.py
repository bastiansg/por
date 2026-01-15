from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger
from pydantic_ai.mcp import MCPServerStreamableHTTP

from por.mcp.server import _get_text_chunk
from por.mcp.utils import process_tool_call
from por.multi_agent.schema import StateSchema
from por.llm_agents import MachiavellianStrategist, MachiavellianStrategistDeps


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("running machiavellian_advisor...")

    mcp = MCPServerStreamableHTTP(
        url="http://por-mcp:8000/mcp",
        process_tool_call=process_tool_call,
    )

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    machiavellian_advisor = MachiavellianStrategist(mcp_servers=[mcp])
    async with machiavellian_advisor.agent:
        advisor_output = await machiavellian_advisor.generate(
            user_prompt="Offer ruthless, strategic advice focusing on power and leverage.",
            agent_deps=MachiavellianStrategistDeps(
                psychological_profile=psychological_profile,
                question=audio_transcription,
                output_language=detected_language,
            ),
        )

    relevant_chunk_ids = advisor_output.relevant_chunk_ids
    logger.info(f"relevant_chunk_ids: {len(relevant_chunk_ids)}")
    chunk_records = (
        _get_text_chunk(chunk_id=chunk_id) for chunk_id in relevant_chunk_ids
    )

    machiavellian_text_chunks = [
        chunk_record.payload["page_content"]
        for chunk_record in chunk_records
        if chunk_record is not None and chunk_record.payload is not None
    ]

    return {
        "machiavellian_advice": advisor_output.machiavellian_advice,
        "machiavellian_text_chunks": machiavellian_text_chunks,
    }


machiavellian_advisor = Node(
    name="machiavellian_advisor",
    run=run,
)
