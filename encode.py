from PIL import Image
import numpy as np

def embed_data(image: Image.Image, data: bytes) -> Image.Image:
    data_len = len(data).to_bytes(4, byteorder='big')
    full_data = data_len + data
    data_bits = ''.join(f'{byte:08b}' for byte in full_data)

    image = image.convert("RGB")
    pixels = np.array(image, dtype=np.uint8)
    flat = pixels.flatten()

    if len(data_bits) > len(flat):
        raise ValueError("Data too large to hide in the image.")

    # Use masking safely to avoid negative values
    for i, bit in enumerate(data_bits):
        flat[i] = (int(flat[i]) & 0b11111110) | int(bit)

    new_pixels = flat.reshape(pixels.shape)
    return Image.fromarray(new_pixels.astype(np.uint8))
