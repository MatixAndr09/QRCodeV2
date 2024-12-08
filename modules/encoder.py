from modules.shape_indicator import detect_data_type, add_indicator
from modules.colorMapping import char_to_color
import numpy as np


def encode_to_qr(text: str, size: int) -> np.ndarray:
    qr_matrix = np.zeros((size, size, 3), dtype=np.uint8)

    # Add indicator and get reserved area
    data_type = detect_data_type(text)
    reserved_area = add_indicator(qr_matrix, data_type)
    x_slice, y_slice = reserved_area

    # Calculate usable area
    current_row = 0
    current_col = y_slice.stop  # Start after reserved area

    # Encode each character
    for char in text:
        color = char_to_color(char)

        # Find next available position
        while current_row < size:
            if current_row < x_slice.stop and current_col < y_slice.stop:
                current_col = y_slice.stop

            if current_col >= size:
                current_row += 1
                current_col = 0
                continue

            # Place the color
            if current_row < size:
                qr_matrix[current_row, current_col] = color
                current_col += 1
                break

            current_col += 1

    return qr_matrix