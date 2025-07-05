import io
import asyncio
import replicate

from PIL import Image
from torchvision import transforms

from multi_agents.graph import Node
from common.logger import get_logger
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing image_generator...")
    conf = config["configurable"]

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    await asyncio.sleep(1)
    sensehat_dsp.start_color_cycle(image_name="si-04")

    await asyncio.sleep(5)
    image_extension = conf["image_extension"]
    output = replicate.run(
        conf["image_generation_model"],
        input={
            "prompt": state.image_generation_prompt.prompt,
            "aspect_ratio": "9:16",
            "output_format": "jpg",
            "safety_filter_level": "block_only_high",
        },
    )

    image_bytes = output.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    resize_transform = transforms.Resize(size=576)
    image = resize_transform(image)

    images_path = conf["images_path"]
    gen_image_path = f"{images_path}/{state.image_id}-gen.{image_extension}"
    image.save(gen_image_path)
    # with open(gen_image_path, "wb") as f:
    #     f.write(output.read())

    return {
        "gen_image_path": gen_image_path,
    }


image_generator = Node(
    name="image_generator",
    run=run,
)
