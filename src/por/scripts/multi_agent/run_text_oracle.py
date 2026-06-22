import uuid
import asyncio

from pathlib import Path

from rich import box
from rich.panel import Panel
from rich.prompt import Prompt

from por.utils.json import save_json
from por.multi_agent import get_multi_agent, get_multi_agent_context
from por.multi_agent.console import console, render_header
from por.multi_agent.schema import StateSchema


EXIT_COMMANDS = {"exit", "quit", "q"}
IMAGE_PATH = (
    Path(__file__).resolve().parents[4] / "resources" / "images" / "bas-13.jpg"
)
STORE_PATH = Path("/resources/states")


def print_panel(
    content: str | None,
    title: str | None,
    border_style: str,
) -> None:
    console.print(
        Panel(
            content or "---",
            title=f"[bold]{title}[/bold]" if title is not None else None,
            title_align="left",
            border_style=border_style,
            box=box.ASCII,
            padding=(1, 2),
        )
    )


def print_result(state: StateSchema) -> None:
    if not state.message_accepted:
        print_panel(
            content=state.rejection_reason,
            title="*** EL ORÁCULO HA RECHAZADO TU CONSULTA ***",
            border_style="bright_red",
        )

        return

    primary_advice = state.nietzsche_advise or state.astrology_advice
    primary_title = (
        "$$ LO QUE DICEN QUE NIETZSCHE DIJO"
        if state.nietzsche_advise is not None
        else "$$ LO QUE DICEN LOS ASTROS"
    )

    print_panel(
        content=primary_advice,
        title=primary_title,
        border_style="bright_magenta",
    )

    if state.satc_advice is not None:
        print_panel(
            content=state.satc_advice,
            title="$$ LO QUE ESCRIBE CARRIE BRADSHAW",
            border_style="bright_cyan",
        )

    song = state.song
    if song is not None:
        print_panel(
            content=(
                f"{song.title} | {song.artist} | {song.year}\n\n"
                f"{state.lyrics_advise}"
            ),
            title="$$ LO QUE TENÉS QUE ESCUCHAR",
            border_style="bright_cyan",
        )

    print_panel(
        content=(
            f"TU LUCKY NUMBER          ::  {state.lucky_number}\n\n"
            f"TU POEMA DOS CORAZONES   ::  {state.selected_dc_poem}\n\n"
            f"TU GALLETA DE LA FORTUNA ::  {state.selected_fc_message}"
        ),
        title=None,
        border_style="white",
    )


async def main() -> None:
    multi_agent = get_multi_agent()
    context = get_multi_agent_context()
    STORE_PATH.mkdir(parents=True, exist_ok=True)

    render_header()
    print_panel(
        content="TYPE  EXIT  /  QUIT  /  Q  TO ESCAPE THE ORACLE",
        title="::: THE ORACLE IS LISTENING :::",
        border_style="bright_cyan",
    )

    while True:
        question = Prompt.ask(
            "\n[bold bright_magenta]YOUR QUESTION ???[/bold bright_magenta]"
        ).strip()

        if question.lower() in EXIT_COMMANDS:
            break

        if not question:
            continue

        image_id = uuid.uuid4().hex
        state = await multi_agent.run(
            input_state={
                "image_id": image_id,
                "image_path": str(IMAGE_PATH),
                "audio_transcription": question,
                "recorder_ok": True,
            },
            context=context,
            thread_id=image_id,
        )

        assert state is not None

        invoked_at = state.invoked_at
        assert invoked_at is not None

        save_json(
            obj=state.model_dump(),
            file_path=str(STORE_PATH / f"{invoked_at}-{image_id}.json"),
        )

        print_result(state)

        console.print()


if __name__ == "__main__":
    asyncio.run(main())
