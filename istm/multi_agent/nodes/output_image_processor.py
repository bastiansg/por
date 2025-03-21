import os

from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from multi_agents.graph import Node
from common.logger import get_logger

from istm.multi_agent.schema import StateSchema, ConfigSchema


IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing output_image_processor...")
    conf = config["configurable"]


output_image_processor = Node(
    name="output_image_processor",
    run=run,
    is_finish_point=True,
)
