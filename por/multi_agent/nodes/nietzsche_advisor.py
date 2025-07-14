from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from pydantic_ai.tools import RunContext
from pydantic_ai.mcp import MCPServerStreamableHTTP, CallToolFunc, ToolResult

from por.llm_agents import NietzscheAdvisor, NietzscheAdvisorDeps
from por.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


async def process_tool_call(
    ctx: RunContext[int],
    call_tool: CallToolFunc,
    tool_name: str,
    args: dict[str, Any],
) -> ToolResult:
    call_result = await call_tool(
        tool_name,
        args,
        metadata={"deps": ctx.deps},
    )

    logger.info(
        {
            "tool": tool_name,
            "args": args,
            "result": call_result,
        }
    )

    return call_result


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing nietzsche_advisor...")
    conf = config["configurable"]

    mcp = MCPServerStreamableHTTP(
        url="http://localhost:8000/mcp",
        process_tool_call=process_tool_call,
    )

    nietzsche_advisor = NietzscheAdvisor(mcp_servers=[mcp])
    nietzsche_advisor_output = await nietzsche_advisor.generate(
        user_prompt="Deliver piercing, symbolic, and transformative insight.",
        agent_deps=NietzscheAdvisorDeps(
            psychological_profile=state.psychological_profile,
            question=state.audio_transcription,
            output_language=conf["output_language"],
        ),
    )

    return {
        "nietzsche_text_chunks": [],
        "nietzsche_advise": nietzsche_advisor_output.nietzsche_advise,
    }


nietzsche_advisor = Node(
    name="nietzsche_advisor",
    run=run,
)
