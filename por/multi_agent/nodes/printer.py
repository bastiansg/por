import asyncio

from escpos.printer import Usb
from multi_agents.graph import Node
from common.logger import get_logger

from por.utils.printer import get_printer
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp


logger = get_logger(__name__)


def head_pipeline(printer: Usb, conf: dict) -> None:
    printer.image(img_source=conf["por_logo_path"])
    printer.text("\n\n")
    printer.text("\n\n")

    printer.set(
        bold=True,
        align="center",
        font=0,
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


def rejection_pipeline(printer: Usb, conf: dict, state: StateSchema) -> None:
    head_pipeline(printer=printer, conf=conf)

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


def main_pipeline(printer: Usb, conf: dict, state: StateSchema) -> None:
    head_pipeline(printer=printer, conf=conf)

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

    printer.set(bold=True)
    printer.block_text("$$ Aire fresco:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.creative_advice)
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text(
        f"$$ Lo que canta {state.selected_song.artist} para vos:"
    )
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
    printer.set(font=1)
    printer.block_text(":) ticket no válido como factura.")

    printer.cut()
    printer.close()


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing printer...")
    conf = config["configurable"]

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    sensehat_dsp.start_color_cycle(image_name="down-arrow")
    printer = get_printer()
    if state.message_accepted:
        main_pipeline(
            printer=printer,
            conf=conf["printer"],
            state=state,
        )

    else:
        rejection_pipeline(
            printer=printer,
            conf=conf["printer"],
            state=state,
        )

    sensehat_dsp.stop()

    await asyncio.sleep(1)
    sensehat_dsp.clear()

    return {
        "print_status": "ok",
    }


printer = Node(
    name="printer",
    run=run,
    is_finish_point=True,
)
