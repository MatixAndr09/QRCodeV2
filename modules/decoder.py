from typing import Tuple
from PIL import Image
import numpy as np


def generate_qr_image(qr_matrix: np.ndarray, back_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
    scale = 10

    scaled = np.repeat(np.repeat(qr_matrix, scale, axis=0), scale, axis=1)
    scaled = scaled.astype(np.uint8)
    return Image.fromarray(scaled)


def decode_qr_image(image_path: str) -> np.ndarray:
    with Image.open(image_path) as image:
        image = image.convert('RGB')
        img_array = np.array(image)
        size = image.size[0] // 10

        qr_matrix = img_array[::10, ::10]
        qr_matrix[np.all(qr_matrix == [255, 255, 255], axis=2)] = 0

        return qr_matrix[:size, :size]


def qr_matrix_to_text(qr_matrix: np.ndarray) -> str:
    text = []

    matrix_flat = qr_matrix.reshape(-1, 3)
    non_zero_mask = np.any(matrix_flat != 0, axis=1)
    bits = non_zero_mask.astype(np.uint8)

    for i in range(0, len(bits), 8):
        chunk = bits[i:i + 8]
        if len(chunk) == 8:
            char_code = int(''.join(map(str, chunk)), 2)
            text.append(chr(char_code))

    return ''.join(text)