from multi_agents.graph import Node
from common.logger import get_logger
from pydantic_ai.mcp import MCPServerStreamableHTTP

from por.mcp.server import get_text_chunk
from por.mcp.utils import process_tool_call
from por.llm_agents import MusicAdvisor, MusicAdvisorDeps
from por.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing music_advisor...")
    conf = config["configurable"]

    collection = "lyrics"
    mcp = MCPServerStreamableHTTP(
        url="http://por-mcp:8000/mcp",
        process_tool_call=process_tool_call,
    )

    music_advisor = MusicAdvisor(mcp_servers=[mcp])
    async with music_advisor.agent.run_mcp_servers():
        music_advisor_output = await music_advisor.generate(
            user_prompt="Provide your pure, poetic, emotionally saturated lyrics.",
            agent_deps=MusicAdvisorDeps(
                collection=collection,
                psychological_profile=state.psychological_profile,
                question=state.audio_transcription,
                output_language=conf["output_language"],
            ),
        )

    relevant_chunk = get_text_chunk(
        collection=collection,
        chunk_id=music_advisor_output.relevant_chunk_id,
    )

    return {
        "music_advice": music_advisor_output.music_advice,
        "selected_song": {
            "title": relevant_chunk.title,
            "artist": relevant_chunk.artist,
            "lyrics": relevant_chunk.text,
        },
    }


music_advisor = Node(
    name="music_advisor",
    run=run,
)
