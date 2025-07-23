from multi_agents.graph import Node
from common.logger import get_logger
from pydantic_ai.mcp import MCPServerStreamableHTTP

from por.mcp.server import get_text_chunk
from por.mcp.utils import process_tool_call
from por.multi_agent.schema import StateSchema, ConfigSchema
from por.llm_agents import NietzscheAdvisor, NietzscheAdvisorDeps


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing nietzsche_advisor...")
    conf = config["configurable"]

    collection = "nietzsche"
    mcp = MCPServerStreamableHTTP(
        url="http://por-mcp:8000/mcp",
        process_tool_call=process_tool_call,
    )

    nietzsche_advisor = NietzscheAdvisor(mcp_servers=[mcp])
    async with nietzsche_advisor.agent.run_mcp_servers():
        nietzsche_advisor_output = await nietzsche_advisor.generate(
            user_prompt="Deliver piercing, symbolic, and transformative insight.",
            agent_deps=NietzscheAdvisorDeps(
                collection=collection,
                psychological_profile=state.psychological_profile,
                question=state.audio_transcription,
                output_language=conf["output_language"],
            ),
        )

    nietzsche_text_chunks = (
        get_text_chunk(
            collection=collection,
            chunk_id=chunk_id,
        )
        for chunk_id in nietzsche_advisor_output.relevant_chunk_ids
    )

    nietzsche_text_chunks = [
        ntc.text for ntc in nietzsche_text_chunks if ntc is not None
    ]

    return {
        "nietzsche_advise": nietzsche_advisor_output.nietzsche_advise,
        "nietzsche_text_chunks": nietzsche_text_chunks,
    }


nietzsche_advisor = Node(
    name="nietzsche_advisor",
    run=run,
)
