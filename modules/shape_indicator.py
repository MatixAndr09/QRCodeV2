from typing import Tuple
from enum import Enum
import numpy as np


class DataType(Enum):
    LINK = ((255, 0, 0), "triangle")  # Red triangle for links
    CODE = ((0, 255, 0), "square")  # Green square for code
    TEXT = ((0, 0, 255), "circle")  # Blue circle for text


def detect_data_type(text: str) -> DataType:
    if text.startswith(("http://", "https://")):
        return DataType.LINK
    elif any(char in text for char in "{}[]();="):
        return DataType.CODE
    return DataType.TEXT


def draw_triangle_outline(matrix: np.ndarray, color: Tuple[int, int, int], pos: Tuple[int, int], size: int):
    x, y = pos
    height = size
    base = size * 2  # Make the base twice as wide as the height

    # Draw the outline of an upward-pointing triangle
    for i in range(height):
        # Calculate the width at this height (reverse the calculation for upward triangle)
        width = (base * i // height)
        start = y + (base - width) // 2

        # Draw left and right edges
        if start < matrix.shape[1]:
            matrix[x + (height - i - 1), start] = color  # Left edge
        if start + width - 1 < matrix.shape[1]:
            matrix[x + (height - i - 1), start + width - 1] = color  # Right edge

        # Draw top edge if we're at the top
        if i == height - 1:
            for j in range(width):
                if start + j < matrix.shape[1]:
                    matrix[x, start + j] = color


def get_reserved_area(matrix_size: int, shape: str, size: int) -> Tuple[slice, slice]:
    """Get the area that should be reserved for the shape indicator."""
    padding = 5
    if shape == "triangle":
        x_start = padding
        x_end = padding + size
        y_start = padding
        y_end = padding + (size * 2)  # Double width for triangle
        return slice(x_start, x_end), slice(y_start, y_end)
    return slice(0, 0), slice(0, 0)


def draw_shape(matrix: np.ndarray, shape: str, color: Tuple[int, int, int], pos: Tuple[int, int], size: int = 40):
    x, y = pos
    if shape == "triangle":
        draw_triangle_outline(matrix, color, pos, size)
    elif shape == "square":
        # Draw square outline
        matrix[x:x + size, y] = color  # Left edge
        matrix[x:x + size, y + size - 1] = color  # Right edge
        matrix[x, y:y + size] = color  # Top edge
        matrix[x + size - 1, y:y + size] = color  # Bottom edge
    elif shape == "circle":
        center = size // 2
        for i in range(size):
            for j in range(size):
                dist = np.sqrt((i - center) ** 2 + (j - center) ** 2)
                if abs(dist - center) < 1:
                    matrix[x + i, y + j] = color


def add_indicator(qr_matrix: np.ndarray, data_type: DataType) -> Tuple[slice, slice]:
    matrix_size = qr_matrix.shape[0]
    if matrix_size < 16:
        return slice(0, 0), slice(0, 0)

    color, shape = data_type.value
    size = min(40, matrix_size // 6)

    # Position in top-left corner with padding
    pos = (5, 5)
    draw_shape(qr_matrix, shape, color, pos, size=size)

    # Return the reserved area
    return get_reserved_area(matrix_size, shape, size)