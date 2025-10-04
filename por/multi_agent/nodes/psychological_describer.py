from typing import Any
from pydantic_extra_types.language_code import LanguageName

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema
from por.llm_agents import PsychologicalDescriber, PsychologicalDescriberDeps

from .utils import get_sensehat_dsp, get_dsp_images


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing psychological_describer...")

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_image_sequence(
        images=[
            dsp_images["si-04a"],
            dsp_images["si-04b"],
        ],
        refresh_rate=0.5,
    )

    image_description = state.image_description
    assert image_description is not None

    question = state.audio_transcription
    assert question is not None

    psychological_describer_agent = PsychologicalDescriber()
    psychological_describer_output = await psychological_describer_agent.generate(
        user_prompt="Provide a psychological profile based on the provided information.",
        agent_deps=PsychologicalDescriberDeps(
            physical_description=image_description.physical_description,
            clothing_description=image_description.clothing_description,
            question=question,
            output_language=LanguageName("English"),
        ),
    )

    sensehat_dsp.stop()
    sensehat_dsp.clear()
    sensehat_dsp.start_color_cycle(dsp_images["si-05"])

    return {
        "psychological_profile": psychological_describer_output.psychological_profile,
    }


psychological_describer = Node(
    name="psychological_describer",
    run=run,
)
