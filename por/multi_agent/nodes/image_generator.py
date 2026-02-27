import io
import base64

from typing import Any
from langgraph.runtime import get_runtime

from PIL import Image
from openai import AsyncOpenAI

from multi_agents.graph import Node
from common.logger import get_logger
from por.multi_agent.schema import StateSchema, ContextSchema

from .utils import get_sensehat_dsp, get_dsp_images


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    logger.info("runing image_generator...")

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_color_cycle(dsp_images["si-07"])

    image_extension = runtime_context.image_extension
    image_generation_prompt = state.image_generation_prompt
    assert image_generation_prompt is not None

    client = AsyncOpenAI()

    try:
        response = await client.responses.create(
            model="gpt-5.2",
            input=image_generation_prompt,
            tools=[
                {
                    "type": "image_generation",
                    "size": "1024x1536",
                    # "size": "1024x1024",
                },
            ],
        )

    except Exception:
        logger.error(f"rejected prompt: {image_generation_prompt}")
        raise

    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]

    image_data = image_data[0]
    assert image_data is not None

    io_bytes = io.BytesIO(base64.b64decode(image_data))
    image = Image.open(io_bytes).convert("RGB")
    # image = image.resize((576, 576), Image.Resampling.LANCZOS)

    padded = Image.new("RGB", (1152, 1536), color=(255, 255, 255))
    x_offset = (1152 - image.width) // 2
    padded.paste(image, (x_offset, 0))
    image = padded.resize((576, 768), Image.Resampling.LANCZOS)

    images_path = runtime_context.images_path
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
