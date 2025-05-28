from functools import lru_cache
from common.logger import get_logger

from rage.retriever import Retriever
from typing import TypeVar, Any

from sensehat_dsp.display import Display


logger = get_logger(__name__)


R = TypeVar("R", bound=dict[str, Any])


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    return Retriever()


def get_str_description(description: dict) -> str:
    people_description_parts = (f"{k}: {v}" for k, v in description.items())
    return "\n".join(people_description_parts)


@lru_cache(maxsize=1)
def get_sensehat_dsp() -> Display:
    return Display()
