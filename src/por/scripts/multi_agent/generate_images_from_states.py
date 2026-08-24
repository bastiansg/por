import asyncio
import io
import json
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

import httpx
from PIL import Image
from pydantic_ai import BinaryContent
from pydantic_extra_types.language_code import LanguageName
from replicate.client import Client
from rich import box
from rich.panel import Panel

from por.llm_agents import (
    ImagePrompter,
    ImagePrompterDeps,
    MicrophoneRemover,
    MicrophoneRemoverDeps,
    PBFImageDescriber,
    PsychologicalDescriber,
    PsychologicalDescriberDeps,
)
from por.multi_agent.config import MultiAgentConfig
from por.multi_agent.console import (
    console,
    render_header,
    render_node_detail,
)
from por.prompt import format_prompt

RESOURCES_PATH = Path(__file__).resolve().parents[4] / "resources"
OUTPUT_PATH = RESOURCES_PATH / "generated-images-selected-states"
SELECTED_STATE_IDS = [
    "b3dfa27c570c45bf9de2465e74f14549",
    "33f3ba371ea14bb28bb7e1814d76d3fe",
    "64e417ad55a74b5e97b21a408fc76892",
    "c6e893ddf8f143c3b868f61296e59107",
    "4886c1ea96294d7caa4d68da6a1a92ec",
    "fe03f987b38c4759bd92b5d3a77234d6",
    "c28843a38efc4230959310b991e8e65c",
    "7e5ac2d79bba4e93b50e5f9194dabcd6",
    "1dde013e329c4750bb4722f3e4e81268",
    "afa1bfea9a8c407b8c37a8eb00278b79",
    "d527401aa1a945ffb617d7df5b1f7e3b",
]


@dataclass(frozen=True)
class StateInput:
    state_id: str
    question: str
    image_path: Path


def _load_state(state_path: Path) -> dict | None:
    with suppress(json.JSONDecodeError, UnicodeDecodeError):
        state = json.loads(state_path.read_text())
        return state if isinstance(state, dict) else None

    return None


def _get_image_paths() -> dict[str, Path]:
    return {
        image_path.name: image_path
        for directory in RESOURCES_PATH.glob("generated-images*")
        if directory.is_dir() and directory != OUTPUT_PATH
        for image_path in directory.iterdir()
        if image_path.is_file()
    }


def _get_valid_inputs() -> dict[str, StateInput]:
    image_paths = _get_image_paths()
    states = (
        state
        for directory in RESOURCES_PATH.glob("states*")
        if directory.is_dir()
        for state_path in directory.glob("*.json")
        if (state := _load_state(state_path)) is not None
    )

    return {
        state_id: StateInput(
            state_id=state_id,
            question=question,
            image_path=image_paths[Path(image_path).name],
        )
        for state in states
        if isinstance((state_id := state.get("image_id")), str)
        if state.get("message_accepted") is True
        if isinstance((question := state.get("audio_transcription")), str)
        if question.strip()
        if isinstance((image_path := state.get("image_path")), str)
        if Path(image_path).name in image_paths
    }


def _get_selected_inputs() -> tuple[StateInput, ...]:
    valid_inputs = _get_valid_inputs()
    invalid_state_ids = tuple(
        state_id
        for state_id in SELECTED_STATE_IDS
        if state_id not in valid_inputs
    )

    if invalid_state_ids:
        raise RuntimeError(
            "Selected states are missing, rejected, or lack a valid image: "
            f"{', '.join(invalid_state_ids)}"
        )

    return tuple(valid_inputs[state_id] for state_id in SELECTED_STATE_IDS)


def _get_media_type(image_path: Path) -> str:
    extension = image_path.suffix.lower().lstrip(".")
    return f"image/{'jpeg' if extension in {'jpg', 'jpeg'} else extension}"


def _save_image(image_data: bytes, image_path: Path) -> None:
    with Image.open(io.BytesIO(image_data)) as source_image:
        image = source_image.convert("L")

    resized_width = 576
    target_height = round(image.height * resized_width / image.width)
    image.resize(
        (resized_width, target_height),
        Image.Resampling.LANCZOS,
    ).save(image_path)


async def _generate_image(
    state_input: StateInput,
    config: MultiAgentConfig,
    replicate_client: Client,
) -> Path:
    image_data = await asyncio.to_thread(state_input.image_path.read_bytes)
    binary_image = BinaryContent(
        data=image_data,
        media_type=_get_media_type(state_input.image_path),
    )

    render_node_detail("status", "Analyzing the source image and question")
    image_description, psychological_profile = await asyncio.gather(
        PBFImageDescriber().generate(
            user_prompt="Analyze the provided image.",
            user_content=binary_image,
        ),
        PsychologicalDescriber().generate(
            user_prompt=(
                "Provide a psychological profile based on the provided information."
            ),
            agent_deps=PsychologicalDescriberDeps(
                question=state_input.question,
                output_language=LanguageName("English"),
            ),
            user_content=binary_image,
        ),
    )

    render_node_detail("status", "Removing microphone references")
    cleaned_description = await MicrophoneRemover().generate(
        user_prompt=(
            "Remove microphone, cable, and held-object references from this "
            "image description."
        ),
        agent_deps=MicrophoneRemoverDeps(
            image_description=image_description,
        ),
    )

    render_node_detail("status", "Creating the image-generation prompt")
    prompt_description = await ImagePrompter().generate(
        user_prompt="Provide the transformed image description.",
        agent_deps=ImagePrompterDeps(
            question=state_input.question,
            psychological_profile=psychological_profile,
            composition=cleaned_description.scene_description.composition,
            people_description=cleaned_description.people_description,
            clothing_description=cleaned_description.clothing_description,
        ),
    )

    image_generation_prompt = format_prompt(
        prompt_description,
        config.caption_header,
    )

    render_node_detail("status", "Generating the image")
    output = await asyncio.to_thread(
        replicate_client.run,
        config.replicate_model,
        wait=False,
        input=(
            config.replicate_input.model_dump()
            | {"prompt": image_generation_prompt}
        ),
    )

    generated_image = next(iter(output))
    generated_image_data = await asyncio.to_thread(generated_image.read)
    output_path = OUTPUT_PATH / (
        f"{state_input.state_id}-gen.{config.replicate_input.output_format}"
    )

    await asyncio.to_thread(_save_image, generated_image_data, output_path)
    return output_path


async def main() -> None:
    selected_inputs = _get_selected_inputs()
    selected_count = len(selected_inputs)

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    config = MultiAgentConfig()
    replicate_client = Client(timeout=httpx.Timeout(config.replicate_timeout))

    render_header()
    console.print(
        Panel(
            (
                f"Loaded {selected_count} selected accepted states.\n"
                f"Output directory: {OUTPUT_PATH}"
            ),
            title="[bold]IMAGE GENERATION[/bold]",
            title_align="left",
            border_style="bright_cyan",
            box=box.ASCII,
            padding=(1, 2),
        )
    )

    for index, state_input in enumerate(
        selected_inputs,
        start=1,
    ):
        console.print(
            Panel(
                state_input.question,
                title=f"[bold]IMAGE {index:02d} OF {selected_count:02d}[/bold]",
                title_align="left",
                border_style="bright_magenta",
                box=box.ASCII,
                padding=(1, 2),
            )
        )

        render_node_detail("state_id", state_input.state_id)
        render_node_detail("source_image", state_input.image_path)
        output_path = await _generate_image(
            state_input,
            config,
            replicate_client,
        )

        render_node_detail("generated_image", output_path)

    console.print(
        Panel(
            (
                f"Generated {selected_count} images.\n"
                f"Output directory: {OUTPUT_PATH}"
            ),
            title="[bold]IMAGE GENERATION COMPLETE[/bold]",
            title_align="left",
            border_style="bright_cyan",
            box=box.ASCII,
            padding=(1, 2),
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
