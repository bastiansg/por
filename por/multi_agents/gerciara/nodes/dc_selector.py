import random

from multi_agents.graph import Node

from common.logger import get_logger
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import dry_mode_handler


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="person_describer",
    return_fields=["selected_dc_poem"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing dc_selector...")
    conf = config["configurable"]

    return {
        "selected_dc_poem": random.choice(conf["dc_poems"])["poem"],
    }


dc_selector = Node(
    name="dc_selector",
    run=run,
)
