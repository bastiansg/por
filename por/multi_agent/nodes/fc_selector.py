import random

from multi_agents.graph import Node

from common.logger import get_logger
from por.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


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
