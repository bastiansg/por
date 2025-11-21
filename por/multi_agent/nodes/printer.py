from typing import Any
from langgraph.runtime import get_runtime

from escpos.printer import Usb
from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema, ContextSchema

from .utils import get_sensehat_dsp, get_dsp_images, get_printer


logger = get_logger(__name__)


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
    printer.block_text("* @dd.moon__                All rights reserved.")
    printer.text("\n\n")

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.set(bold=True, align="left")
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

    printer.set(bold=True)
    printer.block_text("* EL ORÁCULO HA DELIBERADO:")
    printer.set(bold=False)
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("$$ Lo que dicen que Nietzsche dijo:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.nietzsche_advise)
    printer.text("\n\n")

    selected_song = state.selected_song
    assert selected_song is not None

    printer.set(bold=True)
    printer.block_text(f"$$ Lo que canta {selected_song.artist} para vos:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.music_advice)

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.image(
        img_source=state.gen_image_path,
        center=True,
    )

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("Tu lucky number:")
    printer.set(bold=False)
    printer.text("\n")
    printer.block_text(f"{state.lucky_number}")
    printer.text("\n\n")

    # printer.set(bold=True)
    # printer.block_text("Tu poema dos corazones:")
    # printer.set(bold=False)
    # printer.text("\n")
    # printer.block_text(f"{state.selected_dc_poem}")
    # printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("Tu galleta de la fortuna:")
    printer.set(bold=False)
    printer.text("\n")
    printer.block_text(f"{state.selected_fc_message}")
    printer.text("\n\n")
    printer.text("\n\n")

    printer.set(align="center")
    printer.set(font=1)  # type: ignore
    printer.block_text("Ticket no válido como factura :)")

    printer.cut()
    printer.close()


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing printer...")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

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
