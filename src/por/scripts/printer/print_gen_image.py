from pathlib import Path

from por.multi_agent.nodes.utils import get_printer

GENERATED_IMAGES_PATH = Path("/resources/generated-images-selected-states")
IMAGE_EXTENSIONS = {".jpeg", ".jpg", ".png", ".webp"}


def print_generated_images() -> None:
    printer = get_printer()

    image_paths = (
        image_path
        for image_path in sorted(GENERATED_IMAGES_PATH.iterdir())
        if image_path.is_file()
        if image_path.suffix.lower() in IMAGE_EXTENSIONS
    )

    for image_path in image_paths:
        printer.text("\n\n")
        printer.image(
            img_source=str(image_path),
            center=True,
        )

        printer.text("\n\n")
        printer.cut()

    printer.close()


def main() -> None:
    print_generated_images()


if __name__ == "__main__":
    main()
