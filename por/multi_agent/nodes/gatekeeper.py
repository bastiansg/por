from typing import Any
from langgraph.runtime import get_runtime

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import Gatekeeper, GatekeeperDeps
from por.multi_agent.schema import StateSchema, ContextSchema

from .utils import get_sensehat_dsp, get_dsp_images


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing gatekeeper...")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_image_sequence(
        images=[
            dsp_images["si-03a"],
            dsp_images["si-03b"],
        ],
        refresh_rate=0.5,
    )

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    gatekeeper = Gatekeeper()
    gatekeeper_output = await gatekeeper.generate(
        user_prompt=f"Persons's Message: {audio_transcription}",
        agent_deps=GatekeeperDeps(
            output_language=runtime_context.output_language
        ),
    )

    return {
        "message_accepted": gatekeeper_output.message_accepted,
        "rejection_reason": gatekeeper_output.rejection_reason,
    }


gatekeeper = Node(
    name="gatekeeper",
    run=run,
)
