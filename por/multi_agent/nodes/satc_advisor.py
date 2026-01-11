from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger
from pydantic_ai.mcp import MCPServerStreamableHTTP

from por.mcp.server import _get_text_chunk
from por.mcp.utils import process_tool_call
from por.multi_agent.schema import StateSchema
from por.llm_agents import SATCAdvisor, SATCAdvisorDeps


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing satc_advisor...")

    mcp = MCPServerStreamableHTTP(
        url="http://por-mcp:8000/mcp",
        process_tool_call=process_tool_call,
    )

    # psychological_profile = state.psychological_profile
    # assert psychological_profile is not None

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    satc_advisor = SATCAdvisor(mcp_servers=[mcp])
    async with satc_advisor.agent:
        satc_advisor_output = await satc_advisor.generate(
            user_prompt="Speak like Carrie Bradshaw, thinking out loud with a close friend at a restaurant.",
            agent_deps=SATCAdvisorDeps(
                # psychological_profile=psychological_profile,
                question=audio_transcription,
                output_language=detected_language,
            ),
        )

    relevant_chunk_ids = satc_advisor_output.relevant_chunk_ids
    logger.info(f"relevant_chunk_ids: {len(relevant_chunk_ids)}")
    chunk_records = (
        _get_text_chunk(chunk_id=chunk_id) for chunk_id in relevant_chunk_ids
    )

    satc_text_chunks = [
        chunk_record.payload["page_content"]
        for chunk_record in chunk_records
        if chunk_record is not None and chunk_record.payload is not None
    ]

    return {
        "satc_advice": satc_advisor_output.satc_advice,
        "satc_text_chunks": satc_text_chunks,
    }


satc_advisor = Node(
    name="satc_advisor",
    run=run,
)
