import cv2

from PIL import Image

from google import genai  # type: ignore
from google.genai import types

from common.cache import cache, RedisCache


BW_IMAGE_PROMPT = (
    "Convert the provided image into a minimalist black-ink line drawing on a pure white background. "
    "Use no shading, gradients, textures, or cross-hatching. "
    "Keep it flat and 2D, with only outlines and a fixed-width stroke."
)

gemini_client = genai.Client()


def binarize(image_path: str) -> Image.Image:
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

    return Image.fromarray(binary_image)


@cache(redis_cache=RedisCache())
def get_bw_image(image_path: str) -> types.Image:
    image = Image.open(image_path)
    response = gemini_client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[
            BW_IMAGE_PROMPT,
            image,
        ],
    )

    part = response.parts[0]
    image = part.as_image()
    if image is None:
        print(response.parts)

    return image
