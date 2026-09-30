import io
import xml.etree.ElementTree as ET
from typing import Any

import cairosvg
import replicate
from langgraph.runtime import get_runtime
from multi_agents.graph import Node
from PIL import Image, ImageChops

from por.llm_agents import ImagePrompter
from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import ContextSchema, StateSchema

from .utils import get_dsp_images, get_sensehat_dsp


def _crop_svg(svg_bytes: bytes) -> bytes:
    svg = ET.fromstring(svg_bytes)
    view_box = svg.get("viewBox")

    if view_box is None:
        return svg_bytes

    preview_bytes = cairosvg.svg2png(bytestring=svg_bytes)
    with Image.open(io.BytesIO(preview_bytes)).convert("RGBA") as preview:
        background = Image.new("RGBA", preview.size, "white")
        background.alpha_composite(preview)
        grayscale_preview = background.convert("L")

    white_background = Image.new("L", grayscale_preview.size, "white")
    content_bounds = ImageChops.difference(
        grayscale_preview,
        white_background,
    ).getbbox()

    if content_bounds is None:
        return svg_bytes

    view_x, view_y, view_width, view_height = map(
        float,
        view_box.replace(",", " ").split(),
    )

    left, top, right, bottom = content_bounds
    vertical_margin = min(top, grayscale_preview.height - bottom)
    cropped_top = top - vertical_margin
    cropped_bottom = bottom + vertical_margin
    cropped_x = view_x + left * view_width / grayscale_preview.width
    cropped_y = view_y + cropped_top * view_height / grayscale_preview.height
    cropped_width = (right - left) * view_width / grayscale_preview.width
    cropped_height = (
        (cropped_bottom - cropped_top)
        * view_height
        / grayscale_preview.height
    )

    svg.set("viewBox", f"{cropped_x} {cropped_y} {cropped_width} {cropped_height}")
    svg.set("width", str(cropped_width))
    svg.set("height", str(cropped_height))
    return ET.tostring(svg, encoding="utf-8")


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
        user_prompt=(
            "Provide your surreal image-generation prompt."
            f"\n\n**Question**: {audio_transcription}"
            f"\n\n**Psychological Profile**: {psychological_profile}"
            "\n\n**Previous Framing and Viewpoint**: "
            f"{image_description.scene_description.composition}"
            f"\n\n**People Description**: {image_description.people_description}"
            f"\n\n**Clothing Description**: {image_description.clothing_description}"
        ),
    )

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_color_cycle(dsp_images["si-07"])

    image_generation_prompt = ip_output.flux_prompt
    rep_output = await replicate.async_run(
        "recraft-ai/recraft-v4.1-svg",
        input={
            "prompt": image_generation_prompt,
            "size": "896x1152",
        },
    )

    svg_bytes = await rep_output.aread()  # type: ignore
    image_width = 576
    image_margin = 8
    content_width = image_width - image_margin * 2
    cropped_svg_bytes = _crop_svg(svg_bytes)
    png_bytes = cairosvg.svg2png(
        bytestring=cropped_svg_bytes,
        output_width=content_width,
    )

    image = Image.open(io.BytesIO(png_bytes)).convert("L")  # type: ignore

    padded_image = Image.new("L", (image_width, image.height), "white")
    padded_image.paste(image, (image_margin, 0))
    image = padded_image

    images_path = runtime_context.images_path
    invoked_at = state.invoked_at
    assert invoked_at is not None

    gen_image_path = (
        f"{images_path}/{invoked_at}-{state.image_id}-gen."
        f"{generated_image_extension}"
    )
    image.save(gen_image_path)

    return {
        "image_generation_prompt": image_generation_prompt,
        "gen_image_path": gen_image_path,
    }


image_generator = Node(
    name="image_generator",
    run=run,
)
