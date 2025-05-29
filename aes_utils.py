from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

def get_key(password: str) -> bytes:
    return SHA256.new(password.encode()).digest()

def encrypt_bytes(data: bytes, password: str) -> bytes:
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext

def decrypt_bytes(data: bytes, password: str) -> bytes:
    key = get_key(password)
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
