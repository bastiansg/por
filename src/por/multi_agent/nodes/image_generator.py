import asyncio
import io
from pathlib import Path
from typing import Any

import httpx
from langgraph.runtime import get_runtime
from multi_agents.graph import Node
from PIL import Image
from replicate.client import Client

from por.llm_agents import ImagePrompter, ImagePrompterDeps
from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import ContextSchema, StateSchema
from por.prompt import format_prompt

from .utils import get_dsp_images, get_sensehat_dsp


def _resize_image(image_data: bytes, image_path: Path) -> None:
    with Image.open(io.BytesIO(image_data)) as source_image:
        image = source_image.convert("L")

    resized_width = 576
    target_height = round(image.height * resized_width / image.width)
    image = image.resize(
        (resized_width, target_height),
        Image.Resampling.LANCZOS,
    )

    image.save(image_path)


async def run(state: StateSchema) -> dict[str, Any]:
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    render_node_banner("image_generator")

    generated_image_extension = runtime_context.generated_image_extension
    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    psychological_profile = state.psychological_profile
    assert psychological_profile is not None

    image_description = state.image_description
    assert image_description is not None

    ip = ImagePrompter()
    ip_output = await ip.generate(
        user_prompt="Provide the transformed image description.",
        agent_deps=ImagePrompterDeps(
            question=audio_transcription,
            psychological_profile=psychological_profile,
            composition=image_description.scene_description.composition,
            people_description=image_description.people_description,
            clothing_description=image_description.clothing_description,
        ),
    )

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_color_cycle(dsp_images["si-07"])

    image_generation_prompt = format_prompt(
        ip_output,
        runtime_context.caption_header,
    )

    replicate_client = Client(
        timeout=httpx.Timeout(runtime_context.replicate_timeout)
    )

    output = await asyncio.to_thread(
        replicate_client.run,
        runtime_context.replicate_model,
        wait=False,
        input={
            "model": "dev",
            "prompt": image_generation_prompt,
            "lora_scale": 1.3,
            "megapixels": "1",
            "num_outputs": 1,
            "aspect_ratio": "9:16",
            "output_format": generated_image_extension,
            "guidance_scale": 5.0,
            "output_quality": 100,
            "num_inference_steps": 28,
            "disable_safety_checker": True,
        },
    )

    images_path = Path(runtime_context.images_path)
    await asyncio.to_thread(images_path.mkdir, parents=True, exist_ok=True)
    invoked_at = state.invoked_at
    assert invoked_at is not None

    generated_image = next(iter(output))
    image_data = await asyncio.to_thread(generated_image.read)
    gen_image_path = images_path / (
        f"{invoked_at}-{state.image_id}-gen.{generated_image_extension}"
    )

    await asyncio.to_thread(_resize_image, image_data, gen_image_path)

    return {
        "image_description": ip_output,
        "image_generation_prompt": image_generation_prompt,
        "gen_image_path": str(gen_image_path),
    }


image_generator = Node(
    name="image_generator",
    run=run,
)
