from pydantic import BaseSettings, Field


class ConfigDjango(BaseSettings):
    admin_name: str = 'admin'
    admin_pass: str = 'passwd'
    admin_email: str = 'admin@admin.admin'
    secret_key: str = 'django-insecure-j6'


class ConfigRedis(BaseSettings):
    host: str = 'localhost'
    port: int = 6379
    db: int = 0

    class Config:
        env_prefix = 'redis_'


class ConfigDB(BaseSettings):
    host: str = 'localhost'
    port: int = 5432
    dbname: str = Field(..., env='DB_NAME')
    user: str = 'postgres'
    password: str = 'pass'

    class Config:
        env_prefix = 'db_'


class ConfigElk(BaseSettings):
    host: str = 'search'
    port: int = 9200
    indexes: list[str] = ['movies', 'person', 'genre']
    index_schemas: dict[str, str] = {
        'movies': 'es_schema.json',
        'person': 'es_person_schema.json',
        'genre': 'es_genre_schema.json'
    }

    def get_url(self):
        return f'http://{self.host}:{self.port}'

    class Config:
        env_prefix = 'elastic_'


class ConfigElt(BaseSettings):
    limit_film: int = 100
    limit_genre: int = 10
    limit_person: int = 100
    retry_attempt: int = 10
    wait_between_attempt: int = 100
    wait_exp_mult: int = 1
    wait_exp_min: int = 10
    wait_exp_max: int = 600

    class Config:
        env_prefix = 'elt_'


class Config(BaseSettings):
    dev: bool = False
    debug: bool = False

    app: ConfigDjango = ConfigDjango()
    db: ConfigDB = ConfigDB()
    elk: ConfigElk = ConfigElk()
    redis: ConfigRedis = ConfigRedis()
    elt: ConfigElt = ConfigElt()
