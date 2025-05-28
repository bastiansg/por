from pydantic import BaseModel, StrictStr

from common.logger import get_logger
from common.utils.json_data import load_json


logger = get_logger(__name__)


class ImageCaptionItem(BaseModel):
    image_path: StrictStr
    people_description: StrictStr
    scene_description: StrictStr


def image_caption_loader(
    source_path: str = "/resources/data/train-image-captions.json",
) -> list[ImageCaptionItem]:
    return [
        ImageCaptionItem(**ic) for ic in load_json(json_file_path=source_path)
    ]
