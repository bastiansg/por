import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

from hailo_apps.servos import Servos, ServoAngles
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp, get_button


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing idle_state...")
    conf = config["configurable"]

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    await asyncio.sleep(1)
    sensehat_dsp.clear()

    sensehat_dsp.start_intermittent_image(
        image_name="space-invader-4",
        refresh_rate=2.0,
    )

    servos = Servos()
    idle_angles = conf["idle_angles"]
    servos.set_angles(
        servo_angles=ServoAngles(
            x=idle_angles["x"],
            y=idle_angles["y"],
        )
    )

    button = get_button()
    button.wait_for_active()

    sensehat_dsp.stop()
    sensehat_dsp.clear()

    return {
        "button_is_active": True,
    }


idle_state = Node(
    name="idle_state",
    run=run,
    is_entry_point=True,
)
