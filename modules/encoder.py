from modules.shape_indicator import detect_data_type, add_indicator
from concurrent.futures import ThreadPoolExecutor
from modules.colorMapping import char_to_color
import numpy as np


def encode_chunk(chunk: str, start_idx: int, size: int) -> np.ndarray:
    chunk_matrix = np.zeros((size, size, 3), dtype=np.uint8)
    for i, char in enumerate(chunk):
        color = char_to_color(char)
        binary_char = format(ord(char), '08b')
        base_idx = (start_idx + i) * 8

        for j, bit in enumerate(binary_char):
            row = (base_idx + j) // size
            col = (base_idx + j) % size
            if row < size and col < size and int(bit):
                chunk_matrix[row, col] = color
    return chunk_matrix


def encode_to_qr(text: str, size: int) -> np.ndarray:
    qr_matrix = np.zeros((size, size, 3), dtype=np.uint8)
    chunk_size = 1024

    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            futures.append(
                executor.submit(encode_chunk, chunk, i, size)
            )

        for future in futures:
            chunk_matrix = future.result()
            mask = chunk_matrix.any(axis=2)
            qr_matrix[mask] = chunk_matrix[mask]

    # Add data type indicator
    data_type = detect_data_type(text)
    add_indicator(qr_matrix, data_type)

    return qr_matrix
