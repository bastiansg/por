import random

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing number_generator...")

    return {
        "lucky_numbers": [random.randint(0, 45) for _ in range(6)],
    }


number_generator = Node(
    name="number_generator",
    run=run,
)
