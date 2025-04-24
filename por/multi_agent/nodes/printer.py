from multi_agents.graph import Node
from common.logger import get_logger

from por.utils.printer import get_printer
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import dry_mode_handler, get_sensehat_dsp


logger = get_logger(__name__)


def print_pipeline(conf: dict, state: StateSchema) -> None:
    printer = get_printer()
    printer.image(img_source=conf["por_logo_path"])
    printer.text("\n\n")

    printer.set(font=0, double_width=False, double_height=False)
    printer.set(align="left")
    printer.block_text("* Made in Iturri")
    printer.text("\n")
    printer.block_text("* x el Oráculo Robot. (2025, ∞)")
    printer.text("\n")
    printer.block_text("* @dd.moon__                All rights reserved.")
    printer.text("\n\n")
    printer.block_text(f'"{state.selected_dc_poem}"')
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text(
        "* WARNING: Este Robot nunca reemplazará a tu terapeuta.",
    )
    printer.set(bold=False)

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("* EL OJO DEL ORÁCULO HA VISTO LO SIGUIENTE:")
    printer.set(bold=False)
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("$$ Tus deseos:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.person_description.dreams_and_desires)
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("$$ Tus miedos:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.person_description.fears)
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("$$ Sobre el amor:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.person_description.love_status)

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("* EL ORÁCULO HA DELIBERADO:")
    printer.set(bold=False)
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("$$ Sobre tus deseos, dicen que Nietzsche dijo:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.nietzsche_advise)
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("$$ Lo que reveló el Libro Rojo sobre tus miedos:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.jung_advise)
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("$$ Amor: lo que canto Taylor Swift entre líneas:")
    printer.text("\n")
    printer.set(bold=False)

    printer.block_text(state.taylor_swift_advise)

    printer.text("\n\n")
    printer.text("------------------------------------------------")
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("* Y HE AQUÍ TU RETRATO POR @gervasio_ciaravino:")
    printer.text("\n")
    printer.set(bold=False)

    printer.qr(
        content=state.image_url,
        size=8,
        center=True,
    )

    printer.set(bold=True)
    printer.block_text("Tu lucky number:")
    printer.set(bold=False)
    printer.text("\n")
    printer.block_text(f"{state.lucky_number}")
    printer.text("\n\n")

    printer.set(bold=True)
    printer.block_text("El total de tu situación es:")
    printer.set(bold=False)
    printer.text("\n")
    printer.block_text(f"{state.selected_fc_message}")
    printer.text("\n\n")

    printer.set(align="center")
    printer.set(font=1)
    printer.block_text(":) ticket no válido como factura.")

    printer.cut()


@dry_mode_handler(
    func_name="printer",
    return_fields=["printer_job_id"],
)
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
    print_pipeline(conf=conf["printer"], state=state)

    return {
        "print_status": "ok",
    }


printer = Node(
    name="printer",
    run=run,
)
