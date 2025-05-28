import asyncio

from gpiozero import Button
from multi_agents.graph import Node
from common.logger import get_logger

from hailo_apps.servos import Servos, ServoAngles
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing idle_state...")
    conf = config["configurable"]

    sensehat_dsp = get_sensehat_dsp()
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

    idle = True
    button = Button(16)
    while idle:
        await asyncio.sleep(0.01)
        if button.is_pressed:
            idle = False

    del button
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    return {
        "idle": False,
    }


idle_state = Node(
    name="idle_state",
    run=run,
    is_entry_point=True,
)
