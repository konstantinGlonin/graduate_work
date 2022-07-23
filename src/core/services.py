import asyncio
from datetime import datetime

import aiohttp
import aio_pika
from aiohttp import ContentTypeError
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import Config
from models.recomendations import BaseRecommendations

MONGO_CLIENT: AsyncIOMotorClient | None = None
RABBIT_CONNECTION: aio_pika.Connection | None = None

config = Config()


def get_mongo_client():
    return MONGO_CLIENT


def get_rabbit_connection():
    return RABBIT_CONNECTION


async def put_request_on_new_recommendation_into_queue(data: BaseRecommendations, rabbit):
    channel = await rabbit.channel()

    x = await channel.default_exchange.publish(
        aio_pika.Message(body=data.json().encode('utf-8')),
        routing_key="recommendations",
    )
    return x.delivery_tag


async def user_recommendation(data: BaseRecommendations,
                              rabbit=Depends(get_rabbit_connection),
                              mongo=Depends(get_mongo_client)):
    coll = mongo.movies.recommendations
    recommendation = await coll.find_one({"id": f"{data.id}"})

    if recommendation:
        if (datetime.now() - recommendation["updated_at"]).days >= config.recommendation_actuality_duration \
                or recommendation["counter"] >= config.recommendation_counter \
                or recommendation["model_version"] != config.model_version:

            await put_request_on_new_recommendation_into_queue(data=data, rabbit=rabbit)

        _id = recommendation["_id"]
        data_to_mongo = {
            "id": recommendation["id"],
            "type": recommendation["type"],
            "recommendations": recommendation["recommendations"],
            "updated_at": recommendation["updated_at"],
            "model_version": recommendation["model_version"],
            "counter": recommendation["counter"] + 1
        }

        await coll.replace_one({"_id": _id}, data_to_mongo)
        return recommendation["recommendations"]

    return None


async def movie_recommendation():
    pass


async def task(session, url):
    try:
        async with session.get(url=url) as response:
            data = await response.json()
            return data
    except ContentTypeError:
        return None


async def get_top():
    async with aiohttp.ClientSession() as session:

        tasks = [task(session=session, url=config.top_movies_url)]
        top_movies = await asyncio.gather(*tasks)

        return top_movies
