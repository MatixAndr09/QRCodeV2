from typing import Tuple
from enum import Enum
import numpy as np


class DataType(Enum):
    LINK = ((255, 0, 0), "triangle")
    CODE = ((0, 255, 0), "square")
    TEXT = ((0, 0, 255), "circle")


def detect_data_type(text: str) -> DataType:
    if text.startswith(("http://", "https://")):
        return DataType.LINK
    elif any(char in text for char in "{}[]();="):
        return DataType.CODE
    return DataType.TEXT


def draw_shape(matrix: np.ndarray, shape: str, color: Tuple[int, int, int], pos: Tuple[int, int], size: int = 3):
    x, y = pos
    if shape == "square":
        matrix[x:x + size, y:y + size] = color
    elif shape == "triangle":
        for i in range(size):
            matrix[x + i, y + i:y + size - i] = color
    elif shape == "circle":
        center = size // 2
        for i in range(size):
            for j in range(size):
                if (i - center) ** 2 + (j - center) ** 2 <= (size // 2) ** 2:
                    matrix[x + i, y + j] = color


def add_indicator(qr_matrix: np.ndarray, data_type: DataType):
    matrix_size = qr_matrix.shape[0]
    if matrix_size < 16:
        return

    color, shape = data_type.value
    pos = (1, matrix_size - 5)
    draw_shape(qr_matrix, shape, color, pos)