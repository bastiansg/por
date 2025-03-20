import uuid

from time import sleep
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
    face_tracker = FaceTracker(
        init_servo_angles=ServoAngles(**conf["servo_angles"]),
        rotator_params=RotatorParams(**conf["rotator_params"]),
        image_size=ImageSize(**conf["image_size"]),
        history_length=history_length,
        min_score=conf["min_score"],
    )

    face_tracker.run()
    while len(face_tracker.history) < history_length:
        sleep(1)
        pass

    face_tracker.stop()
    history_item = face_tracker.history[-1]

    pil_image = Image.fromarray(history_item.np_image)
    image_id = uuid.uuid4().hex
    image_path = f"{conf['images_path']}/{image_id}.{conf['image_extension']}"

    pil_image.save(image_path)
    return {
        "image_id": image_id,
        "image_path": image_path,
    }


face_tracker = Node(
    name="face_tracker",
    run=run,
    is_entry_point=True,
)
