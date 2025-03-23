import cups

from multi_agents.graph import Node
from common.logger import get_logger

from sensehat_dsp.display import Display
from istm.multi_agent.schema import StateSchema, ConfigSchema

from .utils import dry_mode_handler


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="printer",
    return_fields=["printer_job_id"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing printer...")
    conf = config["configurable"]

    sensehat_dsp = Display()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

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
