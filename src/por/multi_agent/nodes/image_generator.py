import io
import cairosvg
import replicate

from typing import Any
from langgraph.runtime import get_runtime

from PIL import Image

from multi_agents.graph import Node
from rich.console import Console
from por.multi_agent.schema import StateSchema, ContextSchema
from por.llm_agents import ImagePrompter, ImagePrompterDeps

from .utils import get_sensehat_dsp, get_dsp_images


console = Console()


async def run(state: StateSchema) -> dict[str, Any]:
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    console.log("runing image_generator...")

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

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_color_cycle(dsp_images["si-07"])

    image_generation_prompt = ip_output.flux_prompt
    rep_output = replicate.run(
        "recraft-ai/recraft-v4-svg",
        input={
            "prompt": image_generation_prompt,
            "size": "896x1152",
        },
    )

    svg_bytes = rep_output.read()  # type: ignore
    png_bytes = cairosvg.svg2png(bytestring=svg_bytes)
    # image = Image.open(io.BytesIO(png_bytes)).convert("RGB")  # type: ignore
    image = Image.open(io.BytesIO(png_bytes)).convert("L")  # type: ignore
    # image = image.point(lambda p: 255 if p >= 250 else p)  # type: ignore
    # image = image.point(lambda p: 0 if p <= 200 else p)  # type: ignore

    resized_width = 576
    target_height = round(image.height * resized_width / image.width)
    image = image.resize(
        (resized_width, target_height),
        Image.Resampling.LANCZOS,
    )

    images_path = runtime_context.images_path
    invoked_at = state.invoked_at
    assert invoked_at is not None

    gen_image_path = f"{images_path}/{invoked_at}-{state.image_id}-gen.{image_extension}"
    image.save(gen_image_path)

    return {
        "image_generation_prompt": image_generation_prompt,
        "gen_image_path": gen_image_path,
    }


image_generator = Node(
    name="image_generator",
    run=run,
)
