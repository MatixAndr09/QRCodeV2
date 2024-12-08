from modules.colorMapping import color_to_char
from typing import Tuple
from PIL import Image
import numpy as np


def generate_qr_image(qr_matrix: np.ndarray, back_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
    """Generate a QR code image from the matrix."""
    height, width = qr_matrix.shape[:2]

    # Create white background
    background = np.full((height, width, 3), back_color, dtype=np.uint8)

    # Copy non-zero pixels
    mask = np.any(qr_matrix != 0, axis=2)
    background[mask] = qr_matrix[mask]

    # Scale the image
    scale = 10
    scaled = np.repeat(np.repeat(background, scale, axis=0), scale, axis=1)

    # Convert to PIL Image
    qr_image = Image.fromarray(scaled.astype(np.uint8))

    return qr_image


def decode_qr_image(image_path: str) -> np.ndarray:
    """Decode a QR code image to a matrix."""
    with Image.open(image_path) as image:
        image = image.convert('RGB')
        img_array = np.array(image)
        size = image.size[0] // 10

        # Downsample
        qr_matrix = img_array[::10, ::10]
        return qr_matrix[:size, :size]


def qr_matrix_to_text(qr_matrix: np.ndarray) -> str:
    """Convert QR matrix to text."""
    size = qr_matrix.shape[0]
    skip_size = min(45, size // 6)
    text = []

    # Start after the reserved area
    row = 0
    col = skip_size * 2

    while row < size:
        # Get the color at current position
        color = tuple(qr_matrix[row, col])

        # Skip empty (black) pixels
        if any(color):
            char = color_to_char(color)
            if char:  # Only append if we got a valid character
                text.append(char)

        # Move to next position
        col += 1
        if col >= size:
            col = 0
            row += 1
            # Skip reserved area at start of each row
            if row < skip_size and col < skip_size * 2:
                col = skip_size * 2

    # Remove any trailing whitespace
    return ''.join(text).strip()