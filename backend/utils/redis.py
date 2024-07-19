import aioredis
from aioredis import Redis

from settings import REDIS_HOST, REDIS_DB, REDIS_PORT, REDIS_PASSWORD

from .hashing import hash_image


def construct_url():
    if REDIS_PASSWORD:
        return f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    return f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"


def construct_image_key(image_hash: str):
    return f"image:{image_hash}"


def get_connection(func):
    async def wrapper(*args, **kwargs):
        redis = await aioredis.from_url(construct_url())
        try:
            value = await func(redis, *args, **kwargs)
        finally:
            await redis.close()
        return value
    return wrapper


@get_connection
async def save_img_prediction(con: Redis, image_bytes: bytes, image: bytes):
    hashed_image = hash_image(image_bytes)
    await con.set(construct_image_key(hashed_image), image)


@get_connection
async def get_img_prediction(con: Redis, hash_str: str | bytes):
    return await con.get(construct_image_key(hash_str))
