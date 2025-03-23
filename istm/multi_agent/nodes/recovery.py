import uuid
import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

from sensehat_dsp.display import Display
from hailo_apps.servos import Servos, ServoAngles
from istm.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing recovery...")
    conf = config["configurable"]

    sensehat_dsp = Display(refresh_rate=1.0)
    sensehat_dsp.start_intermittent_image(image_name="space-invader-3")

    servos = Servos()
    idle_angles = conf["idle_angles"]
    servos.set_angles(
        servo_angles=ServoAngles(
            x=idle_angles["x"],
            y=idle_angles["y"],
        )
    )

    await asyncio.sleep(conf["recovery_time"])
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    return {
        "image_id": uuid.uuid4().hex,
    }


recovery = Node(
    name="recovery",
    run=run,
)
