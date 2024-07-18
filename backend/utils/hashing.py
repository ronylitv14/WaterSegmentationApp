import hashlib


def hash_image(image_bytes: bytes) -> str:
    return hashlib.sha256(image_bytes).hexdigest()
