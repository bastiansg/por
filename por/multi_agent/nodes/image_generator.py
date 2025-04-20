import replicate

from PIL import Image
from multi_agents.graph import Node
from common.logger import get_logger

from sensehat_dsp.display import Display
from por.multi_agent.schema import StateSchema, ConfigSchema, ConcatImage

from .utils import dry_mode_handler


logger = get_logger(__name__)


def get_concat_image(
    image_path: str,
    gen_image_path: str,
    images_path: str,
    image_id: str,
    image_extension: str,
    margin: int,
) -> ConcatImage:
    image = Image.open(image_path)
    gen_image = Image.open(gen_image_path)

    assert image.width == gen_image.width

    total_width = image.width + 2 * margin
    total_height = image.height + gen_image.height + 3 * margin

    concat_image = Image.new(
        "RGB",
        (total_width, total_height),
        color=(0, 0, 0),
        # color=(255, 255, 255),
    )

    concat_image.paste(image, (margin, margin))
    concat_image.paste(gen_image, (margin, image.height + 2 * margin))

    concat_image_path = f"{images_path}/{image_id}-concat.{image_extension}"
    concat_image.save(concat_image_path)

    width, height = concat_image.size
    return ConcatImage(
        image_path=concat_image_path,
        width=width,
        height=height,
    )


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

    sensehat_dsp = Display(refresh_rate=0.001)
    sensehat_dsp.start_color_cycle(image_name="space-invader-1")

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

    concat_image = get_concat_image(
        image_path=state.image_path,
        gen_image_path=gen_image_path,
        images_path=images_path,
        image_id=image_id,
        image_extension=image_extension,
        margin=conf["image_margin"],
    )

    sensehat_dsp.stop()
    sensehat_dsp.clear()

    return {
        "gen_image_path": gen_image_path,
        "concat_image": concat_image,
    }


image_generator = Node(
    name="image_generator",
    run=run,
)
