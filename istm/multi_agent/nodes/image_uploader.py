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
    logger.info("runing image_uploader...")
    conf = config["configurable"]

    url_endpoint = "https://ik.imagekit.io/ddmoon"
    imagekit = ImageKit(
        public_key=IMAGEKIT_PUBLIC_KEY,
        private_key=IMAGEKIT_PRIVATE_KEY,
        url_endpoint=url_endpoint,
    )

    options = UploadFileRequestOptions(
        folder="/istm",
        is_private_file=False,
    )

    with open(state.gen_image_path, "rb") as image_file:
        upload = imagekit.upload_file(
            file=image_file,
            file_name="test.jpg",
            options=options,
        )


image_uploader = Node(
    name="image_uploader",
    run=run,
    is_finish_point=True,
)
