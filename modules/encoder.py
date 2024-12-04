# modules/encoder.py
import numpy as np
from modules.colorMapping import char_to_color

def encode_to_qr(text, size):
    qr_matrix = np.zeros((size, size, 3), dtype=int)

    if text.startswith("http://") or text.startswith("https://"):
        # Add a green square in the top-right corner
        qr_matrix[0, size-1] = [0, 255, 0]

    for i, char in enumerate(text):
        color = char_to_color(char)
        binary_char = format(ord(char), '08b')
        for j, bit in enumerate(binary_char):
            row = (i * 8 + j) // size
            col = (i * 8 + j) % size
            if int(bit):
                qr_matrix[row, col] = color

    return qr_matrix