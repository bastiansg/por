from pydantic_ai import BinaryContent

from multi_agents.graph import Node
from common.logger import get_logger


from istm.multi_agent.schema import StateSchema, ConfigSchema
from istm.llm_agents import ImageDescriberInput


from .utils import get_image_describer, dry_mode_handler, get_sensehat_dsp


logger = get_logger(__name__)

# "space-invader-1",
# "space-invader-1a",
# "space-invader-1b",
# "space-invader-2",
# "space-invader-3",
# "space-invader-4",
# "space-invader-5",


@dry_mode_handler(
    func_name="image_describer",
    return_fields=["image_description"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing image_describer...")
    conf = config["configurable"]

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.start_intermittent_image(
        image_name="space-invader-1",
        refresh_rate=1,
    )

    image_describer_agent = get_image_describer()
    with open(state.image_path, "rb") as image_file:
        image_describer_output = await image_describer_agent.generate(
            agent_input=ImageDescriberInput(
                description_guidelines=conf["description_guidelines"],
            ),
            user_content=BinaryContent(
                data=image_file.read(),
                media_type=f"image/{conf['image_extension']}",
            ),
        )

    sensehat_dsp.stop()
    sensehat_dsp.clear()

    return {
        "image_description": image_describer_output.description,
    }


image_describer = Node(
    name="image_describer",
    run=run,
)
