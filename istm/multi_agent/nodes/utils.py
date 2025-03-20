from functools import lru_cache
from common.cache import RedisCache

from istm.llm_agents import ImageDescriber


@lru_cache(maxsize=1)
def get_image_describer() -> ImageDescriber:
    return ImageDescriber(cache=RedisCache())
