import asyncio
import functools

from functools import lru_cache
from common.cache import RedisCache
from common.logger import get_logger

from typing import Callable, Awaitable, TypeVar, Any

from istm.llm_agents import ImageDescriber
from istm.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


R = TypeVar("R", bound=dict[str, Any])


@lru_cache(maxsize=1)
def get_image_describer() -> ImageDescriber:
    return ImageDescriber(cache=RedisCache())


def dry_mode_handler(func_name: str, return_fields: list[str]):
    try:

        def decorator(
            func: Callable[[StateSchema, ConfigSchema], Awaitable[R]],
        ) -> Callable[[StateSchema, ConfigSchema], Awaitable[R]]:
            @functools.wraps(func)
            async def wrapper(state: StateSchema, config: ConfigSchema) -> R:
                conf = config["configurable"]
                if conf["dry_mode"]:
                    logger.info(f"runing {func_name} in dry mode...")
                    await asyncio.sleep(conf["dry_mode_wait"])
                    return {field: None for field in return_fields}

                return await func(state, config)

            return wrapper

        return decorator

    except Exception as err:
        raise (err)
