"""Generate captions and numbered image copies for the selected POR images."""

import asyncio
from pathlib import Path
from shutil import copy2

from pydantic_ai import BinaryContent
from rich import box
from rich.console import Console
from rich.panel import Panel

from por.config import config
from por.llm_agents import (
    ImageDescriber,
    ImageDescriberDeps,
    ImageDescriberOutput,
)
from por.prompt import format_prompt

IMAGES_PATH = Path("/resources/por-selected")
OUTPUT_PATH = Path("/resources/por-selected-captioned")
IMAGE_SUFFIX = ".jpg"
IMAGE_MEDIA_TYPE = "image/jpeg"

console = Console()


def print_panel(content: str, title: str, border_style: str) -> None:
    console.print(
        Panel(
            content,
            title=f"[bold]{title}[/bold]",
            title_align="left",
            border_style=border_style,
            box=box.ASCII,
            padding=(1, 2),
        )
    )


def format_caption(description: ImageDescriberOutput) -> str:
    return f"{format_prompt(description, config.caption_header)}\n"


async def run() -> None:
    image_paths = tuple(
        image_path
        for image_path in sorted(IMAGES_PATH.iterdir())
        if image_path.is_file()
        if image_path.suffix.lower() == IMAGE_SUFFIX
    )

    print_panel(
        content=(
            f"IMAGES   :: {IMAGES_PATH}\n"
            f"OUTPUT   :: {OUTPUT_PATH}\n"
            f"COUNT    :: {len(image_paths)}"
        ),
        title="::: IMAGE CAPTION GENERATION :::",
        border_style="bright_cyan",
    )

    if not image_paths:
        return

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    output_image_paths = tuple(
        OUTPUT_PATH / f"{index:02d}{IMAGE_SUFFIX}"
        for index in range(1, len(image_paths) + 1)
    )

    image_data = await asyncio.gather(
        *(
            asyncio.to_thread(image_path.read_bytes)
            for image_path in image_paths
        )
    )

    user_contents = tuple(
        BinaryContent(data=data, media_type=IMAGE_MEDIA_TYPE)
        for data in image_data
    )

    agent_deps = ImageDescriberDeps(flux_max_tokens=config.flux_max_tokens)
    descriptions = await ImageDescriber().batch_generate(
        user_prompts=["Analyze the provided image."] * len(image_paths),
        agent_deps_list=[agent_deps] * len(image_paths),
        user_contents=user_contents,
        cached_generation=True,
    )

    await asyncio.gather(
        *(
            asyncio.to_thread(
                output_image_path.with_suffix(".txt").write_text,
                format_caption(description),
                encoding="utf-8",
            )
            for output_image_path, description in zip(
                output_image_paths,
                descriptions,
                strict=True,
            )
        )
    )

    await asyncio.gather(
        *(
            asyncio.to_thread(copy2, image_path, output_image_path)
            for image_path, output_image_path in zip(
                image_paths,
                output_image_paths,
                strict=True,
            )
        )
    )

    print_panel(
        content=(
            f"SAVED {len(image_paths)} RENAMED IMAGES AND CAPTIONS "
            f"TO {OUTPUT_PATH}"
        ),
        title="::: CAPTION GENERATION COMPLETE :::",
        border_style="bright_magenta",
    )


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
