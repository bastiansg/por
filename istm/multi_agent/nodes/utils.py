import asyncio
import functools

from common.logger import get_logger
from typing import Callable, Awaitable, TypeVar, Any
from istm.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


R = TypeVar("R", bound=dict[str, Any])


def dry_mode_handler(func_name: str, return_fields: list[str]):
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
