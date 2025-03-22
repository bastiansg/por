import asyncio

from PIL import Image
from multi_agents.graph import Node
from common.logger import get_logger

from hailo_apps.apps import FaceTracker
from hailo_apps.servos import ServoAngles
from hailo_apps.meta.interfaces import RotatorParams, ImageSize

from istm.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


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
        min_score=conf["min_score"],
    )

    tracker.run()
    while len(tracker.history) < history_length:
        await asyncio.sleep(1)

    tracker.stop()
    history_item = tracker.history[-1]

    image_id = state.image_id
    pil_image = Image.fromarray(history_item.np_image)

    image_path = f"{conf['images_path']}/{image_id}.{conf['image_extension']}"
    pil_image.save(image_path)

    # FIXME: Why this sleep is necessary to set the angles?
    await asyncio.sleep(1)

    idle_angles = conf["idle_angles"]
    tracker.servos.set_angles(
        servo_angles=ServoAngles(
            x=idle_angles["x"],
            y=idle_angles["y"],
        )
    )

    return {
        "image_path": image_path,
    }


face_tracker = Node(
    name="face_tracker",
    run=run,
    is_entry_point=True,
)
