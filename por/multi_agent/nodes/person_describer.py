from pydantic_ai import BinaryContent

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import PersonDescriber, PersonDescriberInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import dry_mode_handler


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="person_describer",
    return_fields=["person_description"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing person_describer...")
    conf = config["configurable"]

    person_describer_agent = PersonDescriber()
    with open(state.image_path, "rb") as image_file:
        person_describer_output = await person_describer_agent.generate(
            agent_input=PersonDescriberInput(
                description_guidelines=conf["person_description_guidelines"],
                output_language=conf["output_language"],
            ),
            user_content=BinaryContent(
                data=image_file.read(),
                media_type=f"image/{conf['image_extension']}",
            ),
        )

    return {
        "person_description": person_describer_output.model_dump(),
    }


person_describer = Node(
    name="person_describer",
    run=run,
)
