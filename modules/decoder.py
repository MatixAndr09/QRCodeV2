# modules/decoder.py
from PIL import Image
import numpy as np

def generate_qr_image(qr_matrix, back_color=(255, 255, 255)):
    size = qr_matrix.shape[0]
    scale = 10  # Scale factor to enlarge the image
    image = Image.new('RGB', (size * scale, size * scale), back_color)

    for row in range(size):
        for col in range(size):
            if not np.array_equal(qr_matrix[row, col], [0, 0, 0]):
                for i in range(scale):
                    for j in range(scale):
                        image.putpixel((col * scale + j, row * scale + i), tuple(qr_matrix[row, col]))

    return image

# modules/decoder.py
def decode_qr_image(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    size = image.size[0] // 10  # Assuming the scale factor used during encoding was 10
    qr_matrix = np.zeros((size, size, 3), dtype=int)

    for row in range(size):
        for col in range(size):
            pixel = image.getpixel((col * 10, row * 10))
            if pixel != (255, 255, 255):  # Ignore white pixels
                qr_matrix[row, col] = pixel

    return qr_matrix

# modules/decoder.py
def qr_matrix_to_text(qr_matrix):
    size = qr_matrix.shape[0]
    text = ""

    # Check for the green square in the top-right corner
    if np.array_equal(qr_matrix[0, size-1], [0, 255, 0]):
        text += "start "

    for i in range(0, size * size, 8):
        binary_char = ""
        for j in range(8):
            row = (i + j) // size
            col = (i + j) % size
            if row < size and col < size:  # Ensure indices are within bounds
                if not np.array_equal(qr_matrix[row, col], [0, 0, 0]):
                    binary_char += '1'
                else:
                    binary_char += '0'
        char = chr(int(binary_char, 2))
        text += char
    return text