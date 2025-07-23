from multi_agents.graph import Node
from common.logger import get_logger
from pydantic_ai.mcp import MCPServerStreamableHTTP

from por.mcp.server import get_text_chunk
from por.mcp.utils import process_tool_call
from por.multi_agent.schema import StateSchema, ConfigSchema
from por.llm_agents import CreativeAdvisor, CreativeAdvisorDeps


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing creative_advisor...")
    conf = config["configurable"]

    collection = "el-arte-del-pensamiento-creativo"
    mcp = MCPServerStreamableHTTP(
        url="http://por-mcp:8000/mcp",
        process_tool_call=process_tool_call,
    )

    creative_advisor = CreativeAdvisor(mcp_servers=[mcp])
    async with creative_advisor.agent.run_mcp_servers():
        creative_advisor_output = await creative_advisor.generate(
            user_prompt="Provide your energetic and creatively actionable insights.",
            agent_deps=CreativeAdvisorDeps(
                collection=collection,
                psychological_profile=state.psychological_profile,
                question=state.audio_transcription,
                output_language=conf["output_language"],
            ),
        )

    creative_text_chunks = (
        get_text_chunk(
            collection=collection,
            chunk_id=chunk_id,
        )
        for chunk_id in creative_advisor_output.relevant_chunk_ids
    )

    creative_text_chunks = [
        ctc.text for ctc in creative_text_chunks if ctc is not None
    ]

    return {
        "creative_advice": creative_advisor_output.creative_advice,
        "creative_text_chunks": creative_text_chunks,
    }


creative_advisor = Node(
    name="creative_advisor",
    run=run,
)
