import asyncio
from uuid import UUID

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from motor.motor_asyncio import AsyncIOMotorClient
from orjson import orjson

from core.config import Config
from core.services import get_film
from domain.recomendations import Recommendation
from models.collaborative_filter import CollaborativeFilterRecommender
from models.content_based import ContentBasedRecommender

config = Config()
mongodb = AsyncIOMotorClient(config.mongo.host, config.mongo.port)

from models.content_based_model import ContentBasedModel  # noqa
from models.collaborative_filter_model import CollaborativeFilterModel  # noqa

cbr = ContentBasedRecommender(config.cbr_model_path)
cfr = CollaborativeFilterRecommender(config.cfr_model_path)


async def get_movie_recommendations(movie_id: UUID):
    film = await get_film(movie_id)
    if 'genres' not in film:
        return None
    genres = '|'.join([i['name'] for i in film['genres']])
    data = cbr.get_recommends(genres, film['title'])
    data = [i for i in data if str(movie_id) != i]

    if 'detail' in data:
        return None

    return Recommendation(
        id=movie_id,
        type='movie',
        data=data
    )


async def get_user_recommendations(user_id: UUID):
    data = cfr.get_recommends(user_id)

    if len(data) < 0:
        return None

    return Recommendation(
        id=user_id,
        type='user',
        data=data
    )


async def save_recommendations(recommendation: Recommendation):
    coll = mongodb.movies.recommendations

    prev_recommendation = await coll.find_one({"id": f"{recommendation.id}"})
    if prev_recommendation:
        print(f"     Update recomedation for {recommendation.type} {recommendation.id} is: {recommendation.data!r}")
        await coll.replace_one({"_id": prev_recommendation['_id']}, recommendation.safe_dict())
    else:
        print(f"     Create recomedation for {recommendation.type} {recommendation.id} is: {recommendation.data!r}")
        await coll.insert_one(recommendation.safe_dict())


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        event = orjson.loads(message.body.decode())

        if event['type'] == 'movie':
            recommendation = await get_movie_recommendations(event['id'])
        elif event['type'] == 'user':
            recommendation = await get_user_recommendations(event['id'])
        else:
            return None
        if isinstance(recommendation, Recommendation):
            await save_recommendations(recommendation)


async def main() -> None:
    connection = await connect(
        host=config.rabbit.host,
        port=config.rabbit.port,
        password=config.rabbit.password,
        login=config.rabbit.username
    )

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(
            "recommendations",
            durable=True
        )

        await queue.consume(on_message)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
