import asyncio

from common.logger import get_logger
from functools import wraps, lru_cache

from rage.retriever import Retriever
from typing import Callable, Awaitable, TypeVar, Any

from sensehat_dsp.display import Display
from por.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


R = TypeVar("R", bound=dict[str, Any])


def dry_mode_handler(func_name: str, return_fields: list[str]):
    def decorator(
        func: Callable[[StateSchema, ConfigSchema], Awaitable[R]],
    ) -> Callable[[StateSchema, ConfigSchema], Awaitable[R]]:
        @wraps(func)
        async def wrapper(state: StateSchema, config: ConfigSchema) -> R:
            conf = config["configurable"]
            if conf["dry_mode"]:
                logger.info(f"runing {func_name} in dry mode...")
                await asyncio.sleep(conf["dry_mode_wait"])
                return {field: None for field in return_fields}

            return await func(state, config)

        return wrapper

    return decorator


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    return Retriever()


def get_str_person_description(state: StateSchema) -> str:
    person_description_parts = (
        f"{k}: {v}"
        for k, v in state.person_description.model_dump().items()
        if k != "lucky_number"
    )

    return "\n".join(person_description_parts)


@lru_cache(maxsize=1)
def get_sensehat_dsp() -> Display:
    return Display()
