from pydantic import BaseSettings


class MongoSettings(BaseSettings):
    host: str = "mongodb"
    port: int = 27017

    class Config:
        env_prefix = "mongo_"


class RabbitSettings(BaseSettings):
    host: str = "rabbitmq"
    port: int = 5672
    username: str = "user"
    password: str = "as1234"

    class Config:
        env_prefix = "rabbitmq_"


class Config(BaseSettings):
    mongo: MongoSettings = MongoSettings()
    rabbit: RabbitSettings = RabbitSettings()
