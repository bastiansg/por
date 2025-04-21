import uuid
import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

# from hailo_apps.servos import Servos, ServoAngles
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing recovery...")
    conf = config["configurable"]

    await asyncio.sleep(conf["print_wait_time"])
    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    await asyncio.sleep(1)
    refresh_rate = 2.0
    sensehat_dsp.start_intermittent_image(
        image_name="si-04a",
        refresh_rate=refresh_rate,
    )

    await asyncio.sleep(conf["recovery_time"])
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    # asyncio.sleep(refresh_rate)
    # servos = Servos()

    # idle_angles = conf["idle_angles"]
    # servos.set_angles(
    #     servo_angles=ServoAngles(
    #         x=idle_angles["x"],
    #         y=idle_angles["y"],
    #     )
    # )

    return {
        "image_id": uuid.uuid4().hex,
    }


recovery = Node(
    name="recovery",
    run=run,
    is_finish_point=True,
)
