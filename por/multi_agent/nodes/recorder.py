import io
import asyncio

from PIL import Image

from multi_agents.graph import Node
from common.logger import get_logger

from hailo_apps.apps import FaceTracker
from hailo_apps.servos import ServoAngles
from hailo_apps.meta.interfaces import RotatorParams, ImageSize

from por.audio import AudioRecorder
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp, get_button


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing recorder...")
    conf = config["configurable"]

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.start_intermittent_image(
        image_name="heart",
        refresh_rate=0.5,
    )

    audio_recorder = AudioRecorder()
    history_length = conf["history_length"]
    tracker = FaceTracker(
        init_servo_angles=ServoAngles(**conf["servo_angles"]),
        rotator_params=RotatorParams(**conf["rotator_params"]),
        image_size=ImageSize(**conf["image_size"]),
        history_length=history_length,
        min_score=conf["face_detector_min_score"],
    )

    audio_recorder.start()
    tracker.run()

    button = get_button()
    button.wait_for_inactive()

    audio_recorder.stop()
    tracker.stop()
    await asyncio.sleep(2)
    tracker.servos.set_angles(servo_angles=ServoAngles())

    audio_buffer = io.BytesIO()
    audio_recorder.save_to_file(file=audio_buffer)
    audio_buffer.seek(0)

    valid_history_items = [
        history_item
        for history_item in tracker.history
        if history_item.centroid is not None
    ]

    last_history_item = valid_history_items[-1]
    image_id = state.image_id

    pil_image = Image.fromarray(last_history_item.np_image)
    image_path = f"{conf['images_path']}/{image_id}.{conf['image_extension']}"
    pil_image.save(image_path)

    sensehat_dsp.stop()
    await asyncio.sleep(1)
    sensehat_dsp.clear()

    sensehat_dsp.start_intermittent_image(
        image_name="space-invader-2",
        refresh_rate=0.5,
    )

    return {
        "audio_buffer": audio_buffer,
        "image_path": image_path,
    }


recorder = Node(
    name="recorder",
    run=run,
)
