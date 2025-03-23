import qrcode

from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer

from multi_agents.graph import Node
from common.logger import get_logger

from istm.multi_agent.schema import StateSchema, ConfigSchema

from .utils import dry_mode_handler


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="qr_generator",
    return_fields=["qr_image_path"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing qr_generator...")
    conf = config["configurable"]

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=10,
    )

    qr.add_data(state.image_url)
    qr.make(fit=True)

    img = qr.make_image(
        module_drawer=GappedSquareModuleDrawer(size_ratio=0.9),
        fill_color="black",
        back_color="white",
    )

    qr_pil_image = img.get_image()

    # image_size = conf["image_size"]
    # margin = conf["image_margin"]
    # qr_pil_image = qr_pil_image.resize(
    #     (
    #         image_size["width"] + margin,
    #         image_size["height"] + margin,
    #     )
    # )

    images_path = conf["images_path"]
    image_id = state.image_id
    image_extension = conf["image_extension"]

    qr_image_path = f"{images_path}/{image_id}-qr.{image_extension}"
    qr_pil_image.save(qr_image_path)

    return {
        "qr_image_path": qr_image_path,
    }


qr_generator = Node(
    name="qr_generator",
    run=run,
)
