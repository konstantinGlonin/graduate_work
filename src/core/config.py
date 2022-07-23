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
    top_movies_url: str = "http://app:8000/api/v1/films_popular"
    recommendation_counter: int = 5
    recommendation_actuality_duration: int = 7  # in days
    model_version: str = "0.0.1"
    mongo: MongoSettings = MongoSettings()
    rabbit: RabbitSettings = RabbitSettings()
