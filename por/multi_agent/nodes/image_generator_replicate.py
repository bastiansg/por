import io
import replicate
import cairosvg

from typing import Any
from langgraph.runtime import get_runtime

from PIL import Image

from multi_agents.graph import Node
from rich.console import Console
from por.multi_agent.schema import StateSchema, ContextSchema

from .utils import get_sensehat_dsp, get_dsp_images


console = Console()


async def run(state: StateSchema) -> dict[str, Any]:
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    console.log("runing image_generator...")

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_color_cycle(dsp_images["si-07"])

    image_extension = runtime_context.image_extension
    image_generation_prompt = state.image_generation_prompt
    assert image_generation_prompt is not None

    rep_output = replicate.run(
        "recraft-ai/recraft-v4-svg",
        input={
            "prompt": image_generation_prompt,
            "size": "896x1152",
        },
    )

    svg_bytes = rep_output.read()  # type: ignore
    png_bytes = cairosvg.svg2png(bytestring=svg_bytes)
    image = Image.open(io.BytesIO(png_bytes)).convert("RGB")  # type: ignore

    resized_width = 576
    target_height = round(image.height * resized_width / image.width)
    image = image.resize(
        (resized_width, target_height),
        Image.Resampling.LANCZOS,
    )

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
