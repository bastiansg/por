import random

from multi_agents.graph import Node

from common.logger import get_logger
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import dry_mode_handler


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

    return {
        "selected_fc_message": random.choice(conf["fc_messages"])["message"],
    }


fc_selector = Node(
    name="fc_selector",
    run=run,
)
