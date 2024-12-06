# modules/encoder.py
import numpy as np
from modules.colorMapping import char_to_color

def encode_to_qr(text, size):
    qr_matrix = np.zeros((size, size, 3), dtype=int)

    if size > 16 and (text.startswith("http://") or text.startswith("https://")):
        # Add a blue square with a 1-pixel gap from the border and from the 16x16 area
        qr_matrix[1, size-2] = [0, 0, 255]

    for i, char in enumerate(text):
        color = char_to_color(char)
        if color == (0, 0, 0) and char not in [' ', '\n']:  # Assuming black is the default for unsupported chars
            print(f"Character '{char}' is not supported.")
            exit(1)
        binary_char = format(ord(char), '08b')
        for j, bit in enumerate(binary_char):
            row = (i * 8 + j) // size
            col = (i * 8 + j) % size
            if int(bit):
                qr_matrix[row, col] = color

    return qr_matrix