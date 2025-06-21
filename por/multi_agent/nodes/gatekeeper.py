from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import Gatekeeper, GatekeeperInput
from por.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing gatekeeper...")
    conf = config["configurable"]

    gatekeeper = Gatekeeper()
    gatekeeper_output = await gatekeeper.generate(
        agent_input=GatekeeperInput(
            message=state.audio_transcription,
            output_language=conf["output_language"],
        )
    )

    return {
        "message_accepted": gatekeeper_output.message_accepted,
        "rejection_reason": gatekeeper_output.rejection_reason,
    }


gatekeeper = Node(
    name="gatekeeper",
    run=run,
)
