import asyncio
import replicate

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
    output = replicate.run(
        conf["model"],
        input={
            "model": "dev",
            "prompt": state.image_generation_prompt.prompt,
            "go_fast": False,
            "lora_scale": 1.3,
            "megapixels": "1",
            "num_outputs": 1,
            # "aspect_ratio": "4:5",
            "aspect_ratio": "9:16",
            # "height": 1350,
            # "width": 1080,
            "output_format": image_extension,
            "guidance_scale": 10,
            "output_quality": 100,
            "num_inference_steps": 28,
            "disable_safety_checker": True,
        },
    )

    images_path = conf["images_path"]
    image_id = state.image_id

    gen_image_path = f"{images_path}/{image_id}-gen.{image_extension}"
    with open(gen_image_path, "wb") as f:
        f.write(output[0].read())

    return {
        "gen_image_path": gen_image_path,
    }


image_generator = Node(
    name="image_generator",
    run=run,
)
