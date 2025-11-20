from gpiozero import Button
from escpos.printer import Usb
from functools import lru_cache

from common.logger import get_logger

from sensehat_dsp.display import Image
from sensehat_dsp.display import Display

from por.dsp_images import dsp_images


logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_sensehat_dsp() -> Display:
    return Display()


@lru_cache(maxsize=1)
def get_button() -> Button:
    return Button(
        pin=16,
        hold_time=0.001,  # type: ignore
        bounce_time=0.001,
    )


@lru_cache(maxsize=1)
def get_dsp_images():
    return {dsp_image["name"]: Image(**dsp_image) for dsp_image in dsp_images}


def get_printer(profile: str = "TM-T20II") -> Usb:
    return Usb(
        0x04B8,
        0x0E27,
        0,  # type: ignore
        profile=profile,
    )
