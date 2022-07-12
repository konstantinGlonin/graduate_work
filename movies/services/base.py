from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.abstract_cache import AbstractCache
from db.abstract_storage import AbstractStorage
from db.elastic import ElasticStorage, get_elastic
from db.redis import RedisCache, cache_decorator, get_redis
from models.mixin import ListMixin, ModelMixin
from models.params import BaseParamsGrp


class Service:
    def __init__(self, storage: AbstractStorage, cache: AbstractCache):
        self.storage = storage
        self.cache = cache

    @cache_decorator
    async def get(self, obj_id: str, model) -> ModelMixin | None:
        try:
            data = await self.storage.get(obj_id, model)
        except NotFoundError:
            return None
        return data

    @cache_decorator
    async def search(self, params: BaseParamsGrp, model) -> ListMixin | None:
        try:
            data = await self.storage.get_many(params, model)
        except NotFoundError:
            return None

        return data


@lru_cache()
def get_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> Service:
    return Service(
        ElasticStorage(elastic),
        RedisCache(redis)
    )
