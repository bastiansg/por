from gpiozero import Button
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


@lru_cache(maxsize=1)
def get_button() -> Button:
    return Button(
        pin=16,
        hold_time=0.001,
        bounce_time=0.001,
    )
