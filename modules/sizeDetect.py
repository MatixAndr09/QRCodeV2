# modules/sizeDetect.py
import numpy as np

def calculate_qr_size(text_length):
    # Calculate the size of the QR code matrix
    return int(np.ceil(np.sqrt(text_length * 8)))