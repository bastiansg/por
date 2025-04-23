import asyncio
import replicate

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import dry_mode_handler, get_sensehat_dsp


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="image_generator",
    return_fields=[
        "gen_image_path",
        "concat_image_path",
    ],
)
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
    sensehat_dsp.start_color_cycle(
        image_name="si-03",
        refresh_rate=0.001,
    )

    image_size = conf["image_size"]
    output = replicate.run(
        conf["model"],
        input={
            "model": "dev",
            "width": image_size["width"],
            "height": image_size["height"],
            "prompt": state.image_generation_prompt,
            "go_fast": True,
            "lora_scale": 1,
            "megapixels": "1",
            "num_outputs": 1,
            "aspect_ratio": "1:1",
            "output_format": "jpg",
            "guidance_scale": 3,
            "output_quality": 80,
            "prompt_strength": 0.6,
            "extra_lora_scale": 1,
            "num_inference_steps": 28,
            "disable_safety_checker": True,
        },
    )

    images_path = conf["images_path"]
    image_id = state.image_id
    image_extension = conf["image_extension"]

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
