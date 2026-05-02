import cv2

from PIL import Image


def binarize(image_path: str) -> Image.Image:
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

    return Image.fromarray(binary_image)
