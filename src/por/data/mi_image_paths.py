from itertools import cycle


mi_image_paths = [
    "/resources/ticket-images/mi-header-images/mi-01.jpeg",
    "/resources/ticket-images/mi-header-images/mi-02.jpeg",
    "/resources/ticket-images/mi-header-images/mi-03.jpeg",
    "/resources/ticket-images/mi-header-images/mi-04.jpeg",
]

_mi_image_paths_cycle = cycle(mi_image_paths)


def get_mi_image_path() -> str:
    return next(_mi_image_paths_cycle)
