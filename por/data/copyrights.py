from itertools import cycle


copyrights = [
    "All rights unreserved.",
    "All rights lost.",
    "All rights missed.",
    "All rights reversed.",
    "No rights reserved.",
]

_copyrights_cycle = cycle(copyrights)


def get_copyright() -> str:
    return next(_copyrights_cycle)
