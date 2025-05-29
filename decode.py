from PIL import Image
import numpy as np

def extract_data(image: Image.Image) -> bytes:
    pixels = np.array(image.convert("RGB"))
    flat = pixels.flatten()

    length_bits = [str(flat[i] & 1) for i in range(32)]
    length = int(''.join(length_bits), 2)

    total_bits = (length + 4) * 8
    bits = [str(flat[i] & 1) for i in range(total_bits)]

    data = bytes(int(''.join(bits[i:i+8]), 2) for i in range(0, total_bits, 8))
    return data[4:]
