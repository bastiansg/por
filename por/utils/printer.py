from escpos.printer import Usb


def get_printer(profile: str = "TM-T20II") -> Usb:
    return Usb(
        0x04B8,
        0x0E27,
        0,
        profile=profile,
    )
