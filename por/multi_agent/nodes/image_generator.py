import io
import base64
import asyncio

from PIL import Image
from openai import AsyncOpenAI
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

    image_extension = conf["image_extension"]
    image_generation_prompt = conf["imge_generatin_prompt_template"].format(
        psychological_profile=state.psychological_profile,
        physical_description=state.image_description.physical_description,
        clothing_description=state.image_description.clothing_description,
    )

    client = AsyncOpenAI()
    response = await client.responses.create(
        model="gpt-4o-mini",
        input=image_generation_prompt,
        tools=[{"type": "image_generation"}],
    )

    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]

    image_base64 = image_data[0]
    io_bytes = io.BytesIO(base64.b64decode(image_base64))
    image = Image.open(io_bytes).convert("RGB")

    resize_transform = transforms.Resize(size=576)
    image = resize_transform(image)

    images_path = conf["images_path"]
    gen_image_path = f"{images_path}/{state.image_id}-gen.{image_extension}"
    image.save(gen_image_path)

    return {
        "image_generation_prompt": image_generation_prompt,
        "gen_image_path": gen_image_path,
    }


image_generator = Node(
    name="image_generator",
    run=run,
)
