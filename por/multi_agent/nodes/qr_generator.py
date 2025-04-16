import qrcode

from PIL import Image, ImageDraw
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema, ConfigSchema

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
    w, h = qr_pil_image.size

    r_width = state.concat_image.width
    resized_qr_image = Image.new("RGB", (r_width, r_width), "white")

    x_offset = (r_width - w) // 2
    y_offset = (r_width - h) // 2

    resized_qr_image.paste(qr_pil_image, (x_offset, y_offset))
    total_height = resized_qr_image.height + state.concat_image.height
    concat_image = Image.new(
        "RGB",
        (
            resized_qr_image.width,
            total_height,
        ),
        "white",
    )

    concat_image_path = state.concat_image.image_path
    concat_image.paste(
        Image.open(concat_image_path),
        (0, 0),
    )

    concat_image.paste(
        resized_qr_image,
        (0, state.concat_image.height),
    )

    # NOTE: Prevents the printer from auto-cutting the bottom
    draw = ImageDraw.Draw(concat_image)
    draw.rectangle(
        [
            (0, concat_image.height - conf["image_margin"]),
            (concat_image.width, concat_image.height),
        ],
        fill=(0, 0, 0),
    )

    concat_image.save(concat_image_path)
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
