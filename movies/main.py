import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core import config
from core.config import Config
from db import elastic
from db import redis

config = Config()

app = FastAPI(
    title=config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.from_url(
        f"redis://{config.redis.host}:{config.redis.port}", encoding="utf-8", decode_responses=True, db=config.redis.db
    )

    elastic.es = AsyncElasticsearch(hosts=[
        f'http://{config.elastic.host}:{config.elastic.port}'
    ])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['film'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genre'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['person'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
