from PIL import Image

from google import genai  # type: ignore
from google.genai import types

from common.cache import cache, RedisCache


BW_IMAGE_PROPT = "Convert the provided image into a black-and-white image. "

gemini_client = genai.Client()


@cache(redis_cache=RedisCache())
def get_bw_image(image_path: str) -> types.Image:
    image = Image.open(image_path)
    response = gemini_client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[
            BW_IMAGE_PROPT,
            image,
        ],
    )

    part = response.parts[0]
    image = part.as_image()

    return image
