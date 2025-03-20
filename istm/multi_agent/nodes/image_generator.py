import replicate

from multi_agents.graph import Node
from common.logger import get_logger

from istm.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


def parse_image_description(image_description: str) -> str:
    image_description = image_description[:1].lower() + image_description[1:]
    if image_description.endswith("."):
        return image_description

    return f"{image_description}."


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing image_generator...")
    conf = config["configurable"]

    image_description = parse_image_description(state.image_description)
    prompt = f"{conf['generation_prompt_header']} {image_description} {conf['generation_prompt_footer']}"
    logger.info(f"generation_prompt => {prompt}")

    output = replicate.run(
        "bastiansg/gerciara:53881ece494c76b6053387b59210290129dbdafb08c6e5411794255fc34ccfd0",
        input={
            "model": "dev",
            "width": 1024,
            "height": 1024,
            "prompt": prompt,
            "go_fast": False,
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
        },
    )

    gen_image_path = (
        f"{conf['images_path']}/{state.image_id}-gen.{conf['image_extension']}"
    )

    with open(gen_image_path, "wb") as f:
        f.write(output[0].read())

    return {
        "gen_image_path": gen_image_path,
    }


image_generator = Node(
    name="image_generator",
    run=run,
    is_finish_point=True,
)
