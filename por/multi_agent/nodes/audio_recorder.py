import time
import asyncio

from multi_agents.graph import Node
from common.logger import get_logger
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp, get_button, get_audio_recorder


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing audio_recorder...")
    # conf = config["configurable"]

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.start_intermittent_image(
        image_name="heart",
        refresh_rate=1.0,
    )

    audio_recorder = get_audio_recorder()
    audio_recorder.start()

    button = get_button()
    while button.is_pressed:
        await asyncio.sleep(0.01)

    # button.wait_for_inactive()
    # audio_recorder.stop()

    # sensehat_dsp.stop()
    # sensehat_dsp.clear()

    # await asyncio.sleep(1)
    # sensehat_dsp.start_intermittent_image(
    #     image_name="space-invader-2",
    #     refresh_rate=0.5,
    # )

    return {
        "button_is_active": False,
    }


audio_recorder = Node(
    name="audio_recorder",
    run=run,
)
