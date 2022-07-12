import functools
from uuid import UUID

from aioredis import Redis

from core.config import Config
from db.abstract_cache import AbstractCache
from models.mixin import ModelMixin

config = Config()

redis: Redis | None = None


async def get_redis() -> Redis:
    return redis


class RedisCache(AbstractCache):
    def __init__(self, client: Redis):
        self.redis = client

    async def get_from_cache(self, key: str, model: ModelMixin):
        data = await self.redis.get(str(key))

        if not data:
            return None

        return model.parse_raw(data)

    async def load_to_cache(self, key: str, data: ModelMixin) -> None:
        await self.redis.set(str(key), str(data.json()), ex=config.redis.get_expire_time())


def cache_decorator(func):
    @functools.wraps(func)
    async def wrapper(obj, params, model):
        if isinstance(params, UUID):
            key = f'{model.get_index()}::{params}'
        else:
            key = params.rhash()

        data = await obj.cache.get_from_cache(key, model)

        if not data:
            data = await func(obj, params, model)
            if not data:
                return None
            await obj.cache.load_to_cache(key, data)
        return data

    return wrapper
