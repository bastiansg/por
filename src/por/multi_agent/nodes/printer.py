from typing import Any
from langgraph.runtime import get_runtime

from escpos.printer import Usb
from multi_agents.graph import Node
from rich.console import Console

from por.data import get_copyright
from por.multi_agent.schema import StateSchema, ContextSchema

from .utils import get_sensehat_dsp, get_dsp_images, get_printer


console = Console()


RIGHTS_NOTICE_LENGTH = 33


def get_ancora_authors(state: StateSchema) -> list[str]:
    return list(
        dict.fromkeys(
            text_chunk.metadata.author
            for text_chunk in state.ancora_text_chunks
            if text_chunk.metadata.author is not None
        )
    )


def get_ancora_sources_text(state: StateSchema) -> str:
    authors = get_ancora_authors(state=state)
    if not authors:
        return ""

    return f"En base a ideas de: {', '.join(authors)}"


def get_copyright_line():
    _copyright = get_copyright()
    padding_length = RIGHTS_NOTICE_LENGTH - len(_copyright)

    return f"* By @dd.moon__{' ' * padding_length}{_copyright}"


def head_pipeline(
    printer: Usb,
    por_logo_path: str,
    state: StateSchema,
) -> None:
    printer.image(img_source=por_logo_path)
    printer.text("\n\n")
    printer.text("\n\n")

    printer.set(
        bold=True,
        align="center",
        font=0,  # type: ignore
        double_width=False,
        double_height=False,
    )

    printer.set(align="left")
    printer.block_text("* Oráculo Robot. (2025, ∞)")
    printer.text("\n")

    copyright_line = get_copyright_line()
    printer.block_text(copyright_line)
    printer.text("\n\n")

    printer.text("\n")
    printer.image(img_source="/resources/ticket-images/logo-ancora.jpg")

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.set(bold=True, align="center")
    printer.block_text(state.audio_transcription)
    printer.set(bold=False)

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n\n")


def rejection_pipeline(
    printer: Usb,
    por_logo_path: str,
    state: StateSchema,
) -> None:
    head_pipeline(
        printer=printer,
        por_logo_path=por_logo_path,
        state=state,
    )

    printer.set(bold=True, align="center")
    printer.block_text("*** El Oráculo ha rechazado tu consulta ***")
    printer.set(bold=False)

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.block_text(state.rejection_reason)
    printer.text("\n\n")

    printer.cut()
    printer.close()


def main_pipeline(
    printer: Usb,
    por_logo_path: str,
    state: StateSchema,
) -> None:
    head_pipeline(
        printer=printer,
        por_logo_path=por_logo_path,
        state=state,
    )

    printer.set(bold=True, align="left")
    printer.set(bold=True)
    printer.block_text("$$ Inteligencia colectiva:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.ancora_advice)
    printer.text("\n\n")

    ancora_sources_text = get_ancora_sources_text(state=state)
    if ancora_sources_text:
        printer.set(bold=False, align="left")
        printer.block_text(ancora_sources_text)
        printer.text("\n\n")

    #################################################################

    printer.set(bold=True, align="left")
    printer.set(bold=True)
    printer.block_text("$$ Lo que dice Walsh:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.rwalsh_phrase)
    printer.text("\n\n")

    #################################################################

    printer.set(bold=True, align="left")
    printer.set(bold=True)
    printer.block_text("$$ Lo que canta el Indio Solari:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.pr_phrase)
    printer.text("\n\n")

    #################################################################

    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.image(
        img_source=state.gen_image_path,
        center=True,
    )

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n")
    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.text("\n")
    printer.image(img_source="/resources/ticket-images/ancora-red.jpg")

    # printer.set(bold=True)
    # printer.block_text("Tu lucky number:")
    # printer.set(bold=False)
    # printer.text("\n")
    # printer.block_text(f"{state.lucky_number}")
    # printer.text("\n\n")

    # printer.set(bold=True)
    # printer.block_text("Tu poema dos corazones:")
    # printer.set(bold=False)
    # printer.text("\n")
    # printer.block_text(f"{state.selected_dc_poem}")
    # printer.text("\n\n")

    # printer.set(bold=True)
    # printer.block_text("Tu galleta de la fortuna:")
    # printer.set(bold=False)
    # printer.text("\n")
    # printer.block_text(f"{state.selected_fc_message}")
    # printer.text("\n\n")
    # printer.text("\n\n")

    # printer.set(align="center")
    # printer.set(font=1)  # type: ignore
    # printer.block_text("Ticket no válido como factura :)")

    printer.cut()
    printer.close()


async def run(state: StateSchema) -> dict[str, Any]:
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    console.log("runing printer...")

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_color_cycle(dsp_images["down-arrow"])

    printer = get_printer()
    por_logo_path = runtime_context.printer.por_logo_path
    if state.message_accepted:
        main_pipeline(
            printer=printer,
            por_logo_path=por_logo_path,
            state=state,
        )

    else:
        rejection_pipeline(
            printer=printer,
            por_logo_path=por_logo_path,
            state=state,
        )

    sensehat_dsp.stop()
    sensehat_dsp.clear()

    return {
        "print_status": "ok",
    }


printer = Node(
    name="printer",
    run=run,
    is_finish_point=True,
)
