import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import Gatekeeper, GatekeeperDeps
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing gatekeeper...")
    conf = config["configurable"]

    gatekeeper = Gatekeeper()
    gatekeeper_output = await gatekeeper.generate(
        user_prompt=state.audio_transcription,
        agent_deps=GatekeeperDeps(output_language=conf["output_language"]),
    )

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    await asyncio.sleep(1)
    sensehat_dsp.start_intermittent_image(
        image_name="si-02",
        refresh_rate=0.5,
    )

    return {
        "message_accepted": gatekeeper_output.message_accepted,
        "rejection_reason": gatekeeper_output.rejection_reason,
    }


gatekeeper = Node(
    name="gatekeeper",
    run=run,
)
