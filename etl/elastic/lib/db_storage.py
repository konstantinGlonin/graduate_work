from __future__ import annotations

from datetime import datetime
from enum import Enum
from itertools import groupby
from typing import Literal

import psycopg2
from psycopg2.extras import DictCursor

from lib.backoff import backoff
from lib.config import Config
from lib.loader import logger
from lib.models import FilmWork, Person, Genre
from lib.state import State


class ObjectType(Enum):
    FILM = 'film_work'
    PERSON = 'person'
    GENRE = 'genre'


class DbStorage:

    def __init__(self, config: Config):
        self._config = config
        self._connection = None
        self.connect()

    def connected(self) -> bool:
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT 1")
            return True
        except:
            return False

    def connect(self):
        self.close()
        self._connection = psycopg2.connect(**self._config.db.dict(), cursor_factory=DictCursor)

    def close(self):
        if self.connected():
            try:
                self._connection.close()
            except Exception:
                pass

        self._connection = None

    def get_data(self, q: str = ''):
        if not self.connected():
            logger.info('reconnect postgres')
            self.connect()
        cur = self._connection.cursor()
        cur.execute(q)

        return cur.fetchall()

    def get_data_retry(self, q: str = ''):
        return backoff(self.get_data, q)

    def get_modified(self, table: str = None, modified: datetime = None, limit=100):
        where = ''
        if modified is not None:
            where = f"where modified > '{modified}'"

        q = (f'''
            select 
                id, 
                modified
            from content.{table}
            {where}
            order by modified, id desc
            limit {limit} 
        ''')

        return self.get_data_retry(q)

    def get_modified_films_by_films(self, modified: datetime = None, limit=100) -> [set, datetime]:
        data = self.get_modified('film_work', modified, limit)
        if len(data) == 0:
            return set(), modified

        ids = set(i['id'] for i in data)
        max_dt = max([i['modified'] for i in data])

        return ids, max_dt

    def get_modified_films_by(self,
                              object_type: Literal[ObjectType.GENRE, ObjectType.PERSON],
                              modified: datetime = None, limit=10) -> [set, datetime]:
        data = self.get_modified(object_type.value, modified, limit)
        if len(data) == 0:
            return set(), None, modified
        object_ids = ','.join([f"'{i['id']}'" for i in data])
        max_dt = max([i['modified'] for i in data])

        q = f'''
        SELECT 
            fw.id, 
            fw.modified
        FROM content.film_work fw
        LEFT JOIN content.{object_type.value}_film_work pfw ON pfw.film_work_id = fw.id
        WHERE pfw.{object_type.value}_id IN ({object_ids})
        ORDER BY fw.modified, fw.id
        '''

        data = self.get_data_retry(q)

        ids = set(i['id'] for i in data)
        return ids, object_ids, max_dt

    def get_records_info(self, ids: dict):
        ids = ','.join([f"'{i}'" for i in list(ids)])
        q = f'''
        SELECT
            fw.id as fw_id, 
            fw.title, 
            fw.description, 
            fw.rating, 
            fw.type, 
            fw.created, 
            fw.modified, 
            pfw.role, 
            p.id, 
            p.full_name,
            g.name as genre_name,
            gfw.genre_id
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        WHERE fw.id IN ({ids})
        order by fw.id
        '''

        movies = self.get_data_retry(q)

        return movies

    def get_person_data(self, ids):
        if not ids:
            return []
        q = f'''
        SELECT 
            p.id,
            p.full_name,
            pfw.role,
            array_agg(fw.id)::text[] as fw_ids,
            array_agg(fw.title) as title
        FROM content.person p
        JOIN content.person_film_work pfw ON pfw.person_id = p.id
        JOIN content.film_work fw ON fw.id = pfw.film_work_id
        WHERE p.id in ({ids})
        GROUP BY role, p.full_name, p.id;
        '''

        persons = self.get_data_retry(q)

        return persons

    def get_genre_data(self, ids):
        if not ids:
            return []
        q = f'''
        SELECT
            id,
            name,
            description
        FROM content.genre
        WHERE id in ({ids})
        '''

        genres = self.get_data_retry(q)

        return genres

    @staticmethod
    def transform_to_model(data: list):
        movies = []
        for k, g in groupby(data, lambda x: x['fw_id']):
            movies.append(FilmWork.get(g))

        return movies

    @staticmethod
    def transform_to_person_model(data: list):
        persons = []
        for k, g in groupby(sorted(data, key=lambda x: x['id']), key=lambda y: y['id']):
            persons.append(Person.get(g))

        return persons

    def get_modified_films(self, state: State):
        ids = {None}

        while len(ids) > 0:
            films_ids, max_dt_film_work = self.get_modified_films_by_films(state.get_state('max_dt_film_work'),
                                                                           self._config.elt.limit_film)
            genre_films_ids, genre_ids, max_dt_genre = self.get_modified_films_by(ObjectType.GENRE,
                                                                       state.get_state('max_dt_genre'),
                                                                       self._config.elt.limit_genre)
            person_films_ids, person_ids, max_dt_person = self.get_modified_films_by(ObjectType.PERSON,
                                                                         state.get_state('max_dt_person'),
                                                                         self._config.elt.limit_person)

            state.set_state('new_max_dt_film_work', str(max_dt_film_work))
            state.set_state('new_max_dt_person', str(max_dt_person))
            state.set_state('new_max_dt_genre', str(max_dt_genre))

            ids = genre_films_ids | person_films_ids | films_ids

            if len(ids) > 0:
                movies = self.transform_to_model(self.get_records_info(ids))
                persons = self.transform_to_person_model(self.get_person_data(person_ids))
                genres = [Genre(**i) for i in self.get_genre_data(genre_ids)]

                yield movies, persons, genres
