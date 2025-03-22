import cups

from multi_agents.graph import Node
from common.logger import get_logger

from istm.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing printer...")
    conf = config["configurable"]

    cups_connection = cups.Connection()
    printer_job_id = cups_connection.printFile(
        conf["printer_name"],
        state.qr_image_path.__str__(),
        "print",
        {},
    )

    return {
        "printer_job_id": printer_job_id,
    }


printer = Node(
    name="printer",
    run=run,
    is_finish_point=True,
)
