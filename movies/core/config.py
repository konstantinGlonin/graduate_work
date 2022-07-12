import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class RedisSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 6379
    db: int = 0
    cache_expire_in_minutes = 5

    def get_expire_time(self):
        return 60 * int(self.cache_expire_in_minutes)

    class Config:
        env_prefix = 'redis_'


class ElasticSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 9200
    index: str = 'base_index'
    proto: str = 'http'

    def url(self):
        return f'{self.proto}://{self.host}:{str(self.port)}'

    class Config:
        env_prefix = 'elastic_'


class Config(BaseSettings):
    project_name: str = "movies"
    redis: RedisSettings = RedisSettings()
    elastic: ElasticSettings = ElasticSettings()

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
