import random

from multi_agents.graph import Node

from common.logger import get_logger
from por.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing random_selector...")
    conf = config["configurable"]

    return {
        "selected_fc_message": random.choice(conf["fc_messages"])["message"],
        "selected_dc_poem": random.choice(conf["dc_poems"])["poem"],
        "lucky_number": random.randint(1, 22),
    }


random_selector = Node(
    name="random_selector",
    run=run,
)
