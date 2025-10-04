from typing import Any
from langgraph.runtime import get_runtime

from multi_agents.graph import Node
from common.logger import get_logger
from pydantic_ai.mcp import MCPServerStreamableHTTP

from por.mcp.server import _get_text_chunk
from por.mcp.utils import process_tool_call
from por.llm_agents import MusicAdvisor, MusicAdvisorDeps
from por.multi_agent.schema import StateSchema, ContextSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing music_advisor...")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    collection = "lyrics"
    mcp = MCPServerStreamableHTTP(
        url="http://por-mcp:8000/mcp",
        process_tool_call=process_tool_call,
    )

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    music_advisor = MusicAdvisor(mcp_servers=[mcp])
    async with music_advisor.agent:
        music_advisor_output = await music_advisor.generate(
            user_prompt="Provide your pure, poetic, emotionally saturated lyrics.",
            agent_deps=MusicAdvisorDeps(
                collection=collection,
                psychological_profile=psychological_profile,
                question=audio_transcription,
                output_language=runtime_context.output_language,
            ),
        )

    relevant_chunk = _get_text_chunk(
        chunk_id=music_advisor_output.relevant_chunk_id
    )

    assert relevant_chunk is not None

    payload = relevant_chunk.payload
    assert payload is not None

    return {
        "music_advice": music_advisor_output.music_advice,
        "selected_song": {
            "title": payload["metadata"].get("title"),
            "artist": payload["metadata"].get("artist"),
            "lyrics": payload["page_content"],
        },
    }


music_advisor = Node(
    name="music_advisor",
    run=run,
)
