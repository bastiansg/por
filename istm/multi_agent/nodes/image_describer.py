from pydantic_ai import BinaryContent

from multi_agents.graph import Node
from common.logger import get_logger

from istm.multi_agent.schema import StateSchema, ConfigSchema
from istm.llm_agents import ImageDescriberInput


from .utils import get_image_describer


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing image_describer...")
    conf = config["configurable"]

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

    return {
        "image_description": image_describer_output.description,
    }


image_describer = Node(
    name="image_describer",
    run=run,
)
