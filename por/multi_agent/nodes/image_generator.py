import io
import base64

from typing import Any
from langgraph.runtime import get_runtime

from PIL import Image
from openai import AsyncOpenAI

from multi_agents.graph import Node
from common.logger import get_logger
from por.multi_agent.schema import StateSchema, ContextSchema
from por.llm_agents import ImagePrompter, ImagePrompterDeps

from .utils import get_sensehat_dsp, get_dsp_images


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    logger.info("runing image_generator...")

    image_extension = runtime_context.image_extension
    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    psychological_profile = state.psychological_profile
    assert psychological_profile is not None

    image_description = state.image_description
    assert image_description is not None

    ip = ImagePrompter()
    ip_output = await ip.generate(
        user_prompt="Provide your surreal image-generation prompt.",
        agent_deps=ImagePrompterDeps(
            question=audio_transcription,
            psychological_profile=psychological_profile,
            physical_description=image_description.physical_description,
            clothing_description=image_description.clothing_description,
        ),
    )

    image_generation_prompt = ip_output.flux_prompt
    client = AsyncOpenAI()

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_color_cycle(dsp_images["si-07"])

    try:
        response = await client.images.generate(
            model="gpt-image-1",
            # model="gpt-image-1-mini",
            prompt=image_generation_prompt,
            moderation="low",
            quality="high",
            size="1024x1536",
        )

    except Exception:
        logger.error(f"rejected prompt: {image_generation_prompt}")
        raise

    response_data = response.data
    assert response_data is not None

    image_data = response_data[0].b64_json
    assert image_data is not None

    io_bytes = io.BytesIO(base64.b64decode(image_data))
    image = Image.open(io_bytes).convert("RGB")

    resized_width = 400
    padded_width = 576

    target_height = round(image.height * resized_width / image.width)
    image = image.resize(
        (resized_width, target_height),
        Image.Resampling.LANCZOS,
    )

    padded_image = Image.new("RGB", (padded_width, target_height), "white")
    x_offset = (padded_width - resized_width) // 2
    padded_image.paste(image, (x_offset, 0))
    image = padded_image

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
