import asyncio
from uuid import UUID

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from orjson import orjson

from core.config import Config
from core.services import get_top

config = Config()


async def get_movie_recommendations(movie_id: UUID):
    # todo: replace by model prediction
    return await get_top()


async def get_user_recommendations(user_id: UUID):
    # todo: replace by model prediction
    return await get_top()


async def save_recommendations(event: dict, recommendations: dict):
    # todo: replace by model prediction
    print(f"     Recomedation for {event['type']} {event['id']} is: {recommendations!r}")


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        event = orjson.loads(message.body.decode())

        if event['type'] == 'movie':
            recommendations = await get_movie_recommendations(event['id'])
        elif event['type'] == 'user':
            recommendations = await get_user_recommendations(event['id'])
        else:
            return None
        await save_recommendations(event, recommendations)


async def main() -> None:
    connection = await connect(
        host=config.rabbit.host,
        port=config.rabbit.port,
        password=config.rabbit.password,
        login=config.rabbit.username
    )
    # todo: Добавить инициализацию ML моделей и подключение к MongoDB

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
