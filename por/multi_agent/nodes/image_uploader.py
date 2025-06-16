import os
# import asyncio

# from imagekitio import ImageKit
# from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema, ConfigSchema

# from .utils import get_sensehat_dsp


IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing image_uploader...")
    conf = config["configurable"]

    # sensehat_dsp = get_sensehat_dsp()
    # sensehat_dsp.stop()
    # sensehat_dsp.clear()

    # await asyncio.sleep(1)
    # sensehat_dsp.start_color_cycle(image_name="up-arrow")

    # url_endpoint = conf["imagekit_url"]
    # imagekit = ImageKit(
    #     public_key=IMAGEKIT_PUBLIC_KEY,
    #     private_key=IMAGEKIT_PRIVATE_KEY,
    #     url_endpoint=url_endpoint,
    # )

    # options = UploadFileRequestOptions(
    #     folder="/por",
    #     is_private_file=False,
    # )

    # gen_image_path = state.gen_image_path
    # image_name = os.path.basename(gen_image_path)
    # with open(gen_image_path, "rb") as image_file:
    #     upload = imagekit.upload_file(
    #         file=image_file,
    #         file_name=image_name,
    #         options=options,
    #     )

    # image_url = f"{url_endpoint}{upload.file_path}"
    return {
        "image_url": None,
    }


image_uploader = Node(
    name="image_uploader",
    run=run,
)
