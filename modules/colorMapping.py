from functools import lru_cache
import numpy as np

@lru_cache(maxsize=1)
def get_color_array():
    color_array = np.zeros((128, 3), dtype=np.uint8)

    COLORS = {
        range(ord('a'), ord('z') + 1): np.array([
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
            (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0),
            (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128),
            (192, 192, 192), (128, 128, 128), (64, 64, 64), (192, 0, 0),
            (0, 192, 0), (0, 0, 192), (192, 192, 0), (192, 0, 192),
            (0, 192, 192), (64, 0, 0), (0, 64, 0), (0, 0, 64),
            (64, 64, 0), (64, 0, 64)
        ]),
        range(ord('A'), ord('Z') + 1): np.array([
            (255, 128, 0), (128, 255, 0), (0, 255, 128), (0, 128, 255),
            (128, 0, 255), (255, 0, 128), (255, 128, 128), (128, 255, 128),
            (128, 128, 255), (255, 255, 128), (255, 128, 255), (128, 255, 255),
            (192, 128, 128), (128, 192, 128), (128, 128, 192), (192, 192, 128),
            (192, 128, 192), (128, 192, 192), (64, 128, 128), (128, 64, 128),
            (128, 128, 64), (64, 64, 128), (64, 128, 64), (128, 64, 64),
            (192, 64, 64), (64, 192, 64)
        ]),
        range(ord('0'), ord('9') + 1): np.array([
            (64, 64, 192), (192, 192, 64), (192, 64, 192), (64, 192, 192),
            (255, 64, 64), (64, 255, 64), (64, 64, 255), (255, 255, 64),
            (255, 64, 255), (64, 255, 255)
        ])
    }

    SPECIAL_CHARS = {
        '!': (192, 255, 64), '@': (255, 192, 64), '#': (64, 192, 255),
        '$': (192, 64, 255), '%': (255, 64, 192), '^': (64, 255, 192),
        '&': (192, 255, 192), '*': (255, 192, 192), '(': (192, 192, 255),
        ')': (255, 192, 255), '-': (192, 255, 255), '_': (64, 64, 64),
        '=': (128, 128, 128), '+': (192, 192, 192), '[': (255, 255, 255),
        ']': (0, 0, 0), '{': (128, 0, 0), '}': (0, 128, 0),
        '|': (0, 0, 128), '\\': (128, 128, 0), ':': (128, 0, 128),
        ';': (0, 128, 128), '"': (192, 192, 0), '\'': (192, 0, 192),
        '<': (0, 192, 192), '>': (64, 0, 0), ',': (0, 64, 0),
        '.': (0, 0, 64), '?': (64, 64, 0), '/': (64, 0, 64)
    }

    for char_range, colors in COLORS.items():
        for i, char_code in enumerate(char_range):
            color_array[char_code] = colors[i]

    for char, color in SPECIAL_CHARS.items():
        color_array[ord(char)] = color

    return color_array


def char_to_color(char: str) -> tuple:
    """Convert a character to a unique RGB color."""
    # Use a simple hash function to generate consistent RGB values
    char_code = ord(char)
    r = (char_code * 7) % 256
    g = (char_code * 11) % 256
    b = (char_code * 13) % 256
    return (r, g, b)


def color_to_char(color: tuple) -> str:
    """Convert an RGB color back to a character."""
    # Find the character that would generate this color
    for i in range(128):  # ASCII range
        test_color = char_to_color(chr(i))
        if test_color == tuple(color):
            return chr(i)
    return ''