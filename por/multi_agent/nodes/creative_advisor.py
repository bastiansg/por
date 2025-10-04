from typing import Any
from langgraph.runtime import get_runtime

from multi_agents.graph import Node
from common.logger import get_logger
from pydantic_ai.mcp import MCPServerStreamableHTTP

from por.mcp.server import _get_text_chunk
from por.mcp.utils import process_tool_call
from por.multi_agent.schema import StateSchema, ContextSchema
from por.llm_agents import CreativeAdvisor, CreativeAdvisorDeps


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing creative_advisor...")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    collection = "el-arte-del-pensamiento-creativo"
    mcp = MCPServerStreamableHTTP(
        url="http://por-mcp:8000/mcp",
        process_tool_call=process_tool_call,
    )

    creative_advisor = CreativeAdvisor(mcp_servers=[mcp])
    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    async with creative_advisor.agent:
        creative_advisor_output = await creative_advisor.generate(
            user_prompt="Provide your energetic and creatively actionable insights.",
            agent_deps=CreativeAdvisorDeps(
                collection=collection,
                psychological_profile=psychological_profile,
                question=audio_transcription,
                output_language=runtime_context.output_language,
            ),
        )

    relevant_chunk_ids = creative_advisor_output.relevant_chunk_ids
    logger.info(f"relevant_chunk_ids: {len(relevant_chunk_ids)}")

    chunk_records = (
        _get_text_chunk(chunk_id=chunk_id) for chunk_id in relevant_chunk_ids
    )

    creative_text_chunks = [
        chunk_record.payload["page_content"]
        for chunk_record in chunk_records
        if chunk_record is not None and chunk_record.payload is not None
    ]

    return {
        "creative_advice": creative_advisor_output.creative_advice,
        "creative_text_chunks": creative_text_chunks,
    }


creative_advisor = Node(
    name="creative_advisor",
    run=run,
)
