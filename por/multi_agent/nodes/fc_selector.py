from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import FCSelector, FCSelectorInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import dry_mode_handler, get_str_person_description


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="person_describer",
    return_fields=["selected_fc_message"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing fc_selector...")
    conf = config["configurable"]

    fc_messages = conf["fc_messages"]
    fc_message_map = {
        message["message_id"]: message["message"] for message in fc_messages
    }

    str_person_description = get_str_person_description(state=state)
    fc_selector = FCSelector()
    fc_selector_output = await fc_selector.generate(
        agent_input=FCSelectorInput(
            person_description=str_person_description,
            fc_messages=fc_messages,
        )
    )

    return {
        "selected_fc_message": fc_message_map[fc_selector_output.message_id],
    }


fc_selector = Node(
    name="fc_selector",
    run=run,
)
