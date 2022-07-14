from motor.motor_asyncio import AsyncIOMotorClient


MONGO_CLIENT: AsyncIOMotorClient | None = None


def get_mongo_client():
    return MONGO_CLIENT
