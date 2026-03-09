from typing import Any
from datetime import datetime
from langgraph.runtime import get_runtime

from escpos.printer import Usb
from multi_agents.graph import Node
from common.logger import get_logger

from por.data import get_copyright
from por.multi_agent.schema import StateSchema, ContextSchema

from .utils import get_sensehat_dsp, get_dsp_images, get_printer


logger = get_logger(__name__)


RIGHTS_NOTICE_LENGTH = 36


def get_copyright_line():
    _copyright = get_copyright()
    padding_length = RIGHTS_NOTICE_LENGTH - len(_copyright)

    return f"* @dd.moon__{' ' * padding_length}{_copyright}"


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
    current_year = datetime.now().year
    printer.block_text(f"* Oráculo Robot. ({current_year}, ∞)")
    printer.text("\n")

    copyright_line = get_copyright_line()
    printer.block_text(copyright_line)
    printer.text("\n\n")

    # printer.text("\n")
    # printer.image(
    #     img_source="/resources/ticket-images/material-interactions-576.jpg"
    # )

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
    printer.block_text("$$ Lo que dicen que Nietzsche dijo:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.nietzsche_advise)
    printer.text("\n\n")

    printer.set(bold=True, align="left")
    printer.set(bold=True)
    printer.block_text("$$ Lo que escribe Carrie Bradshaw:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.satc_advice)
    printer.text("\n\n")

    printer.set(bold=True, align="left")
    printer.set(bold=True)
    printer.block_text("$$ Lo que tenés que escuchar:")
    printer.set(bold=False)
    printer.text("\n\n")

    song_text = f"{state.song.title} | {state.song.artist} | {state.song.year}"  # type: ignore
    printer.block_text(song_text)
    printer.text("\n\n")
    printer.block_text(state.lyrics_advise)  # type: ignore

    printer.text("\n\n")

    # printer.set(bold=True, align="left")
    # printer.set(bold=True)
    # printer.block_text("$$ El plan de Maquiavelo:")
    # printer.text("\n")
    # printer.set(bold=False)

    # printer.block_text(state.machiavelli_advice)
    # printer.text("\n\n")

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

    printer.set(bold=True)
    printer.block_text("Tu poema dos corazones:")
    printer.set(bold=False)
    printer.text("\n")
    printer.block_text(f"{state.selected_dc_poem}")
    printer.text("\n\n")

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
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    logger.info("runing printer...")

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
