import hashlib
from uuid import UUID

from pydantic import BaseModel


class ShortModel(BaseModel):
    id: UUID
    name: str

    def __hash__(self):
        return hash(self.id)


class ShortFilm(BaseModel):
    id: UUID
    title: str

    def __hash__(self):
        return hash(self.id)


class Genre(ShortModel):
    description: str = None


class Person(ShortModel):
    film_ids: list[str] | None = None

    actor: list[ShortFilm] | None = None
    writer: list[ShortFilm] | None = None
    director: list[ShortFilm] | None = None

    @classmethod
    def get(cls, data):
        person = {
            'film_ids': set()
        }
        for row in data:
            person['id'] = row['id']
            person['name'] = row['full_name']
            if role := row['role']:
                for film_id in row['fw_ids']:
                    person['film_ids'].add(film_id)
                person[role] = [
                    ShortFilm(
                        id=fw_id,
                        title=title
                    ) for fw_id, title in list(zip(row['fw_ids'], row['title']))
                ]

        return cls(**person)


class FilmWork(BaseModel):
    """Schema describe Film work instance,
    which will migrate into ElasticSearch"""

    id: UUID
    imdb_rating: float | None = None
    title: str
    description: str | None = None

    theme_md5: str = ''

    genres: list[ShortModel] | None = None
    director: list[ShortModel] | None = None
    actors: list[ShortModel] | None = None
    writers: list[ShortModel] | None = None

    genres_id: list[str] | None = None
    actors_id: list[str] | None = None
    writers_id: list[str] | None = None
    director_id: list[str] | None = None
    persons_id: list[str] | None = None

    @classmethod
    def get(cls, data):

        film = {
            'genres': set(),
            'genres_id': set(),
            'director': set(),
            'actors': set(),
            'writers': set(),
            'actors_id': set(),
            'writers_id': set(),
            'director_id': set(),
            'persons_id': set()
        }
        theme = set()
        for row in data:

            film['id'] = row['fw_id']
            film['title'] = row['title']
            film['imdb_rating'] = row['rating']
            film['description'] = row['description']
            film['genres'].add(ShortModel(id=row['genre_id'], name=row['genre_name']))
            film['genres_id'].add(row['genre_id'])

            if row['role'] == 'director':
                film['director'].add(ShortModel(id=row['id'], name=row['full_name']))
                film['director_id'].add(row['id'])
                film['persons_id'].add(row['id'])
            if row['role'] == 'actor':
                film['actors'].add(ShortModel(id=row['id'], name=row['full_name']))
                film['actors_id'].add(row['id'])
                film['persons_id'].add(row['id'])
            if row['role'] == 'writer':
                film['writers'].add(ShortModel(id=row['id'], name=row['full_name']))
                film['writers_id'].add(row['id'])
                film['persons_id'].add(row['id'])

            theme.add(str(row['genre_name']))

        film['theme_md5'] = hashlib.md5(''.join(sorted(theme)).encode('utf-8')).hexdigest()

        return cls(**film)
