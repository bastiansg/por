from multi_agents.graph import Node
from common.logger import get_logger

from por.audio import AudioRecorder
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing audio_recorder...")
    conf = config["configurable"]

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.start_intermittent_image(image_name="heart", refresh_rate=1.0)

    audio_recorder = AudioRecorder()
    audio_recorder.start()

    return {
        "image_path": image_path,
    }


audio_recorder = Node(
    name="audio_recorder",
    run=run,
)
