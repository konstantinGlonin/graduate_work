import time

import redis as redis
import requests

from lib.backoff import backoff
from lib.config import Config
from lib.db_storage import DbStorage
from lib.loader import Loader
from lib.log import logger
from lib.state import State, JsonFileStorage, RedisStorage


def commit_state():
    state.copy_state('new_max_dt_film_work', 'max_dt_film_work')
    state.copy_state('new_max_dt_person', 'max_dt_person')
    state.copy_state('new_max_dt_genre', 'max_dt_genre')


def check_service(url: str = None):
    logger.warning('Wait elastic start')
    resp = requests.get(url)
    if resp.ok:
        logger.info('Elastik load')


if __name__ == '__main__':
    config = Config()
    redis = redis.Redis(**config.redis.dict())
    logger.info("Start migration")

    storage = RedisStorage(redis)
    # storage = JsonFileStorage('data.json')
    state = State(storage)

    if config.debug:
        state.clear_state()

    backoff(check_service, config.elk.get_url())

    loader = Loader(config)
    psql = DbStorage(config)

    j = 0
    while True:
        j += 1
        i = 0
        for films, persons, genres in psql.get_modified_films(state):

            if i == 0:
                logger.info("Job start")

            backoff(loader.save_data, films, 'movies')
            if persons:
                backoff(loader.save_data, persons, 'person')
            if genres:
                backoff(loader.save_data, genres, 'genre')
            commit_state()

            i = i + 1
        if i > 0:
            logger.info("Job done")

        if j % 2 == 0:
            logger.info('tack')
        else:
            logger.info('tick')
        time.sleep(config.elt.wait_between_attempt)
