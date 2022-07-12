from elasticsearch import AsyncElasticsearch, NotFoundError

from db.abstract_storage import AbstractStorage

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    return es


class ElasticStorage(AbstractStorage):
    def __init__(self, client):
        self.elastic = client

    async def get(self, obj_id, model):

        try:
            data = await self.elastic.get(index=model.get_index(), id=obj_id)
            data = model.fill_elk(data)

            if not data:
                return None
        except NotFoundError:
            return None

        return data

    async def get_many(self, params, model):

        try:
            data = await self.elastic.search(**params.to_elk())
            data = model.fill_elk(data)

            if not data:
                return None
        except NotFoundError:
            return None

        return data
