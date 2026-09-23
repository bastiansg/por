import asyncio
from collections.abc import Callable
from functools import partial
from time import monotonic
from typing import Any, cast

from escpos.printer import Usb
from langgraph.runtime import get_runtime
from multi_agents.graph import Node
from usb.core import Device, USBTimeoutError

from por.data import get_copyright
from por.meta.astrology_symbols import astrology_symbols_image
from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import ContextSchema, StateSchema

from .utils import get_dsp_images, get_printer, get_sensehat_dsp

PRINT_COMPLETION_COMMAND = b"\x1d\x72\x01"
PRINT_COMPLETION_STATUS_MASK = 0b11110000
PRINT_COMPLETION_STATUS_VALUE = 0
PRINT_COMPLETION_TIMEOUT = 30.0


def print_and_wait(
    printer: Usb,
    print_job: Callable[[Usb], None],
) -> None:
    print_job(printer)
    printer._raw(PRINT_COMPLETION_COMMAND)

    device = printer.device
    if device is None:
        raise RuntimeError("The printer USB connection is not open")

    device = cast(Device, device)
    deadline = monotonic() + PRINT_COMPLETION_TIMEOUT
    raw_status = None
    while raw_status is None:
        remaining_timeout = deadline - monotonic()
        if remaining_timeout <= 0:
            raise TimeoutError(
                "The printer did not confirm completion within "
                f"{PRINT_COMPLETION_TIMEOUT} seconds"
            )

        try:
            response = device.read(
                endpoint=printer.in_ep,
                size_or_buffer=16,
                timeout=max(1, round(remaining_timeout * 1000)),
            )

        except USBTimeoutError as error:
            raise TimeoutError(
                "The printer did not confirm completion within "
                f"{PRINT_COMPLETION_TIMEOUT} seconds"
            ) from error

        raw_status = next(
            (
                int(value)
                for value in response
                if (int(value) & PRINT_COMPLETION_STATUS_MASK)
                == PRINT_COMPLETION_STATUS_VALUE
            ),
            None,
        )


def head_pipeline(
    printer: Usb,
    por_logo_path: str,
    state: StateSchema,
) -> None:
    printer.image(img_source=por_logo_path)
    printer.text("\n\n")
    printer.text("\n\n")

    printer.set(
        bold=False,
        align="center",
        font=0,  # type: ignore
        double_width=False,
        double_height=False,
    )

    printer.set(align="left")
    printer.block_text("* Oráculo Robot. (2025, ∞)")
    printer.text("\n")

    printer.text("* By ")
    printer.set(bold=True)
    printer.text("@dd.moon__")
    printer.set(bold=False)
    printer.text("\n")

    printer.text("* Drawings by ")
    printer.set(bold=True)
    printer.text("@paulabelenfa")
    printer.set(bold=False)
    printer.text("\n\n")

    printer.block_text(get_copyright())
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
    close_printer: bool = True,
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
    if close_printer:
        printer.close()


def main_pipeline(
    printer: Usb,
    por_logo_path: str,
    state: StateSchema,
    close_printer: bool = True,
) -> None:
    head_pipeline(
        printer=printer,
        por_logo_path=por_logo_path,
        state=state,
    )

    nietzsche_advise = state.nietzsche_advise
    astrology_advice = state.astrology_advice

    header = (
        "$$ Lo que dicen que Nietzsche dijo:"
        if nietzsche_advise is not None
        else "$$ Lo que dicen los astros:"
    )

    message = (
        nietzsche_advise if nietzsche_advise is not None else astrology_advice
    )

    printer.set(bold=True, align="left")
    printer.set(bold=True)
    printer.block_text(header)
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(message)
    printer.text("\n\n")

    if nietzsche_advise is None:
        astrology_placements = state.astrology_placements
        assert astrology_placements is not None

        with astrology_symbols_image(
            sun=astrology_placements.sun,
            moon=astrology_placements.moon,
            rising=astrology_placements.rising,
        ) as astrology_image_path:
            printer.image(
                img_source=astrology_image_path,
                center=True,
            )

    printer.text("\n")

    #################################################################

    if state.satc_advice is not None:
        printer.set(bold=True, align="left")
        printer.set(bold=True)
        printer.block_text("$$ Lo que escribe Carrie Bradshaw:")
        printer.text("\n")
        printer.set(bold=False)

        printer.block_text(state.satc_advice)
        printer.text("\n\n")

    #################################################################

    if state.song is not None and state.lyrics_advise is not None:
        printer.set(bold=True, align="left")
        printer.set(bold=True)
        printer.block_text("$$ Lo que tenés que escuchar:")
        printer.set(bold=False)
        printer.text("\n")

        song_text = (
            f"{state.song.title} | {state.song.artist} | {state.song.year}"
        )

        printer.block_text(song_text)
        printer.text("\n\n")
        printer.block_text(state.lyrics_advise)
        printer.text("\n\n")

    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.image(
        img_source=state.gen_image_path,
        center=True,
    )

    printer.image(
        img_source="/resources/ticket-images/pbfa-sign.png",
        center=True,
    )

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n")
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
    printer.set(bold=True)
    printer.block_text(state.image_id)
    printer.set(bold=False)
    printer.text("\n\n")
    printer.block_text("Ticket no válido como factura (:")

    printer.cut()
    if close_printer:
        printer.close()


async def run(state: StateSchema) -> dict[str, Any]:
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    render_node_banner("printer")

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_color_cycle(dsp_images["down-arrow"])

    printer = get_printer()
    por_logo_path = runtime_context.printer.por_logo_path
    pipeline = main_pipeline if state.message_accepted else rejection_pipeline
    print_job = partial(
        pipeline,
        por_logo_path=por_logo_path,
        state=state,
        close_printer=False,
    )

    try:
        await asyncio.to_thread(print_and_wait, printer, print_job)
    finally:
        printer.close()

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
