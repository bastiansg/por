import os

from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from multi_agents.graph import Node
from common.logger import get_logger

from sensehat_dsp.display import Display
from istm.multi_agent.schema import StateSchema, ConfigSchema

from .utils import dry_mode_handler


IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="image_uploader",
    return_fields=["image_url"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing image_uploader...")
    conf = config["configurable"]

    sensehat_dsp = Display(refresh_rate=0.25)
    sensehat_dsp.start_intermittent_image(image_name="space-invader-2")

    url_endpoint = conf["imagekit_url_endpoint"]
    imagekit = ImageKit(
        public_key=IMAGEKIT_PUBLIC_KEY,
        private_key=IMAGEKIT_PRIVATE_KEY,
        url_endpoint=url_endpoint,
    )

    options = UploadFileRequestOptions(
        folder="/istm",
        is_private_file=False,
    )

    concat_image_path = state.concat_image.image_path
    image_name = os.path.basename(concat_image_path)
    with open(concat_image_path, "rb") as image_file:
        upload = imagekit.upload_file(
            file=image_file,
            file_name=image_name,
            options=options,
        )

    image_url = f"{url_endpoint}{upload.file_path}"
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    return {
        "image_url": image_url,
    }


image_uploader = Node(
    name="image_uploader",
    run=run,
)
