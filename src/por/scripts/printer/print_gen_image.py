import argparse
from pathlib import Path

from por.multi_agent.nodes.utils import get_printer


GENERATED_IMAGES_PATH = Path("/resources/generated-images")


def print_gen_image(gen_image_path: str) -> None:
    image_path = GENERATED_IMAGES_PATH / gen_image_path
    printer = get_printer()
    printer.text("\n\n")
    printer.image(
        img_source=str(image_path),
        center=True,
    )

    printer.text("\n\n")
    printer.cut()
    printer.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a generated image.")
    parser.add_argument(
        "--gen-image-path",
        required=True,
        help="Path to the generated image.",
    )
    args = parser.parse_args()

    print_gen_image(gen_image_path=args.gen_image_path)


if __name__ == "__main__":
    main()
