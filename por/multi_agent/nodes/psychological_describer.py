import asyncio

# from pydantic_ai import BinaryContent

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import PsychologicalDescriber, PsychologicalDescriberInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import get_sensehat_dsp


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing psychological_describer...")
    conf = config["configurable"]

    psychological_describer_agent = PsychologicalDescriber()
    psychological_describer_output = (
        await psychological_describer_agent.generate(
            agent_input=PsychologicalDescriberInput(
                people_description=state.image_description.people_description,
                scene_description=state.image_description.scene_description,
                output_language=conf["output_language"],
            )
        )
    )

    # with open(state.image_path, "rb") as image_file:
    #     psychological_describer_output = (
    #         await psychological_describer_agent.generate(
    #             agent_input=PsychologicalDescriberInput(
    #                 output_language=conf["output_language"],
    #             ),
    #             user_content=BinaryContent(
    #                 data=image_file.read(),
    #                 media_type=f"image/{conf['image_extension']}",
    #             ),
    #         )
    #     )

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    await asyncio.sleep(1)
    sensehat_dsp.start_intermittent_image(
        image_name="si-02",
        refresh_rate=0.5,
    )

    return {
        "psychological_description": psychological_describer_output,
    }


psychological_describer = Node(
    name="psychological_describer",
    run=run,
)
