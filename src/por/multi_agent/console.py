import json

from itertools import cycle
from typing import Any

from rich.align import Align
from rich.console import Console
from rich.text import Text


console = Console()


POR_BANNER = (
    "██████╗  ██████╗ ██████╗ ",
    "██╔══██╗██╔═══██╗██╔══██╗",
    "██████╔╝██║   ██║██████╔╝",
    "██╔═══╝ ██║   ██║██╔══██╗",
    "██║     ╚██████╔╝██║  ██║",
    "╚═╝      ╚═════╝ ╚═╝  ╚═╝",
)
POR_STYLES = (
    "bold bright_magenta",
    "bold magenta",
    "bold bright_cyan",
)
NODE_ACTIONS = {
    "astrology_advisor": "READING THE STARS",
    "astrology_placements_extractor": "LOOKING FOR YOUR SUN / MOON / RISING",
    "audio_transcriber": "TURNING YOUR VOICE INTO TEXT",
    "gatekeeper": "CHECKING YOUR QUESTION AT THE DOOR",
    "idle_state": "WAITING FOR A SIGN",
    "image_describer": "LOOKING AT YOU",
    "image_generator": "MAKING YOUR VISION VISIBLE",
    "language_detector": "LISTENING FOR YOUR LANGUAGE",
    "lyrics_advisor": "DIGGING FOR YOUR SONG",
    "nietzsche_advisor": "ASKING NIETZSCHE",
    "printer": "PRINTING YOUR TICKET",
    "psychological_describer": "READING BETWEEN YOUR LINES",
    "random_selector": "LEAVING SOMETHING TO CHANCE",
    "recorder": "RECORDING YOUR QUESTION",
    "satc_advisor": "ASKING CARRIE BRADSHAW",
    "validation_checkpoint": "DECIDING WHAT COMES NEXT",
}


def render_header() -> None:
    banner = Text(justify="center")
    for line, style in zip(POR_BANNER, cycle(POR_STYLES), strict=False):
        banner.append(f"{line}\n", style=style)

    banner.append(
        "P O P   O R A C L E   R O B O T",
        style="dim bright_magenta",
    )

    console.print(Align.center(banner))


def render_node_banner(node_name: str) -> None:
    action = NODE_ACTIONS[node_name]
    label = node_name.replace("_", " ").upper()
    message = Text()
    message.append("\n┌─[ ", style="dim magenta")
    message.append(f"{label} ]\n", style="bold white")
    message.append("└──> ", style="dim magenta")
    message.append(f"{action}...\n", style="dim white")

    console.print(message)


def render_node_detail(
    label: str,
    value: object,
) -> None:
    detail = Text()
    detail.append(" :: ", style="dim magenta")
    detail.append(
        label.replace("_", " ").upper(),
        style="bold white",
    )
    detail.append(" // ", style="dim magenta")
    detail.append(str(value), style="dim white")

    console.print(detail)


def render_tool_call(
    tool_name: str,
    parameters: dict[str, Any],
) -> None:
    label = tool_name.replace("_", " ").upper()
    formatted_parameters = json.dumps(
        parameters,
        ensure_ascii=False,
        indent=2,
        default=str,
    )
    message = Text()
    message.append("\n┌─[ ", style="dim magenta")
    message.append(f"TOOL // {label} ]\n", style="bold white")
    message.append("├── ", style="dim magenta")
    message.append("PARAMETERS\n", style="dim white")

    for line in formatted_parameters.splitlines():
        message.append("│   ", style="dim magenta")
        message.append(f"{line}\n", style="dim white")

    message.append("└──> ", style="dim magenta")
    message.append("INVOKING TOOL...\n", style="dim white")

    console.print(message)
