import asyncio
import statistics

from PIL import Image
from collections import deque
from more_itertools import unzip

from multi_agents.graph import Node
from common.logger import get_logger

from hailo_apps.apps import FaceTracker
from hailo_apps.servos import ServoAngles
from hailo_apps.meta.interfaces.rotator_app import HistoryItem
from hailo_apps.meta.interfaces import RotatorParams, ImageSize

from sensehat_dsp.display import Display
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp


logger = get_logger(__name__)


def tracker_is_active(
    tracker_history: deque[HistoryItem],
    history_length: int,
    sensehat_dsp: Display,
) -> bool:
    if len(tracker_history) < history_length:
        return True

    x_deltas, y_deltas = unzip(
        (
            history_item.x_delta,
            history_item.y_delta,
        )
        for history_item in tracker_history
    )

    delta_avg = statistics.mean(
        [
            statistics.mean(x_deltas),
            statistics.mean(y_deltas),
        ]
    )

    logger.info(f"delta_avg => {delta_avg}")
    sensehat_dsp.refresh_rate = delta_avg

    if delta_avg > 0:
        return True

    return False


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing face_tracker...")
    conf = config["configurable"]

    history_length = conf["history_length"]
    tracker = FaceTracker(
        init_servo_angles=ServoAngles(**conf["servo_angles"]),
        rotator_params=RotatorParams(**conf["rotator_params"]),
        image_size=ImageSize(**conf["image_size"]),
        history_length=history_length,
        min_score=conf["face_detector_min_score"],
    )

    gol_colors = conf["gol_colors"]
    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.start_gol(
        p_color=gol_colors["p_color"],
        s_color=gol_colors["s_color"],
        refresh_rate=1.0,
    )

    tracker.run()
    is_active = True
    while is_active:
        is_active = tracker_is_active(
            tracker_history=tracker.history,
            history_length=history_length,
            sensehat_dsp=sensehat_dsp,
        )

        await asyncio.sleep(1)

    tracker.stop()
    tracker.servos.set_angles(servo_angles=ServoAngles())

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
    sensehat_dsp.clear()

    await asyncio.sleep(1)
    sensehat_dsp.start_intermittent_image(
        image_name="si-01",
        refresh_rate=0.5,
    )

    return {
        "image_path": image_path,
    }


face_tracker = Node(
    name="face_tracker",
    run=run,
    is_entry_point=True,
)
