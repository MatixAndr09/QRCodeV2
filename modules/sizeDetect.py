from functools import lru_cache
import numpy as np

@lru_cache(maxsize=128)
def calculate_qr_size(text_length: int) -> int:
    min_bits = text_length * 8
    base_size = int(np.ceil(np.sqrt(min_bits)))

    return base_size + (base_size % 2)