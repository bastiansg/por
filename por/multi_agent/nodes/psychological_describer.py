import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import PsychologicalDescriber, PsychologicalDescriberDeps
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing psychological_describer...")
    # conf = config["configurable"]

    psychological_describer_agent = PsychologicalDescriber()
    psychological_describer_output = await psychological_describer_agent.generate(
        user_prompt="Provide a psychological profile.",
        agent_deps=PsychologicalDescriberDeps(
            physical_description=state.image_description.physical_description,
            clothing_description=state.image_description.clothing_description,
            question=state.audio_transcription,
        ),
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
        "psychological_profile": psychological_describer_output.psychological_profile,
    }


psychological_describer = Node(
    name="psychological_describer",
    run=run,
)
