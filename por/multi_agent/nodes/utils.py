from functools import lru_cache
from common.logger import get_logger

from rage.retriever import Retriever
from sensehat_dsp.display import Display


logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    return Retriever()


@lru_cache(maxsize=1)
def get_sensehat_dsp() -> Display:
    return Display()
