import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema, ConfigSchema
from por.llm_agents import ASCIIImageGenerator, ASCIIImageGeneratorDeps

from .utils import get_sensehat_dsp


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing ascii_image_generator...")
    # conf = config["configurable"]

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    await asyncio.sleep(1)
    sensehat_dsp.start_color_cycle(image_name="si-04")

    aig = ASCIIImageGenerator()
    aig_output = await aig.generate(
        user_prompt="Provide an ASCII image.",
        agent_deps=ASCIIImageGeneratorDeps(
            question=state.audio_transcription,
            psychological_profile=state.psychological_profile,
            physical_description=state.image_description.physical_description,
            clothing_description=state.image_description.clothing_description,
        ),
    )

    return {
        "ascii_image": aig_output.ascii_image,
    }


ascii_image_generator = Node(
    name="ascii_image_generator",
    run=run,
)
