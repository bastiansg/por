from typing import Any
from langgraph.runtime import get_runtime

from multi_agents.graph import Node
from common.logger import get_logger
from pydantic_ai.mcp import MCPServerStreamableHTTP

from por.mcp.server import _get_text_chunk
from por.mcp.utils import process_tool_call
from por.multi_agent.schema import StateSchema, ContextSchema
from por.llm_agents import NietzscheAdvisor, NietzscheAdvisorDeps


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing nietzsche_advisor...")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    collection = "nietzsche"
    mcp = MCPServerStreamableHTTP(
        url="http://por-mcp:8000/mcp",
        process_tool_call=process_tool_call,
    )

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    nietzsche_advisor = NietzscheAdvisor(mcp_servers=[mcp])
    async with nietzsche_advisor.agent:
        nietzsche_advisor_output = await nietzsche_advisor.generate(
            user_prompt="Deliver piercing, symbolic, and transformative insight.",
            agent_deps=NietzscheAdvisorDeps(
                collection=collection,
                psychological_profile=psychological_profile,
                question=audio_transcription,
                output_language=runtime_context.output_language,
            ),
        )

    relevant_chunk_ids = nietzsche_advisor_output.relevant_chunk_ids
    logger.info(f"relevant_chunk_ids: {len(relevant_chunk_ids)}")
    chunk_records = (
        _get_text_chunk(chunk_id=chunk_id) for chunk_id in relevant_chunk_ids
    )

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
