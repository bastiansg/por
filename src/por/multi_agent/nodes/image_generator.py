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
from por.multi_agent.console import render_node_banner, render_node_detail
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

    generated_image_extension = runtime_context.replicate_input.output_format
    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    psychological_profile = state.psychological_profile
    assert psychological_profile is not None

    image_description = state.image_description
    assert image_description is not None

    ip = ImagePrompter()
    ip_output = await ip.generate(
        user_prompt=(
            "Provide the transformed image description."
            f"\n\n**Question**: {audio_transcription}"
            f"\n\n**Psychological Profile**: {psychological_profile}"
            "\n\n**Previous Framing and Viewpoint**: "
            f"{image_description.scene_description.composition}"
            f"\n\n**People Description**: {image_description.people_description}"
            f"\n\n**Clothing Description**: {image_description.clothing_description}"
        ),
        agent_deps=ImagePrompterDeps(
            flux_max_tokens=runtime_context.flux_max_tokens,
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

    image_generation_prompt_tokens = ip_output.count_prompt_tokens(
        runtime_context.caption_header,
        runtime_context.t5_tokenizer_name,
    )

    render_node_detail(
        "image_generation_prompt_tokens",
        image_generation_prompt_tokens,
    )

    replicate_client = Client(
        timeout=httpx.Timeout(runtime_context.replicate_timeout)
    )

    output = await asyncio.to_thread(
        replicate_client.run,
        runtime_context.replicate_model,
        wait=False,
        input=(
            runtime_context.replicate_input.model_dump()
            | {"prompt": image_generation_prompt}
        ),
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
