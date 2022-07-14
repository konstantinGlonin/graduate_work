from uuid import UUID

from models.genre import ShortGenre
from models.mixin import IndexType, ListMixin, ModelMixin
from models.person import ShortPerson


class ShortFilm(ModelMixin):
    _index: IndexType = IndexType.MOVIES

    id: UUID
    title: str
    imdb_rating: float = 0

    class Config:
        schema_extra = {
            "example": {
                "id": "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
                "title": "Star Wars: Episode IV - A New Hope",
                "imdb_rating": 7
            }
        }


class ShortFilms(ListMixin):
    __model__: ShortFilm = ShortFilm
    __root__: list[ShortFilm] = []

    class Config:
        schema_extra = {
            "example": [
                {
                    "id": "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
                    "title": "Star Wars: Episode IV - A New Hope",
                    "imdb_rating": 7
                }
            ]
        }


class Film(ShortFilm):
    id: UUID
    title: str
    imdb_rating: float = 0
    description: str = None

    genres: list[ShortGenre] = []

    director: list[ShortPerson] = []
    actors: list[ShortPerson] = []
    writers: list[ShortPerson] = []

    class Config:
        schema_extra = {
            "example": {
                "id": "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
                "title": "Star Wars: Episode IV - A New Hope",
                "imdb_rating": 8.6,
                "description": "The Imperial Forces, under orders from cruel Darth Vader, hold Princess Leia hostage in their efforts to quell the rebellion against the Galactic Empire. Luke Skywalker and Han Solo, captain of the Millennium Falcon, work together with the companionable droid duo R2-D2 and C-3PO to rescue the beautiful princess, help the Rebel Alliance and restore freedom and justice to the Galaxy.",
                "genres": [
                    {
                        "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
                        "name": "Fantasy"
                    },
                    {
                        "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                        "name": "Action"
                    },
                    {
                        "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
                        "name": "Sci-Fi"
                    },
                    {
                        "id": "120a21cf-9097-479e-904a-13dd7198c1dd",
                        "name": "Adventure"
                    }
                ],
                "director": [
                    {
                        "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
                        "name": "George Lucas"
                    }
                ],
                "actors": [
                    {
                        "id": "b5d2b63a-ed1f-4e46-8320-cf52a32be358",
                        "name": "Carrie Fisher"
                    },
                    {
                        "id": "e039eedf-4daf-452a-bf92-a0085c68e156",
                        "name": "Peter Cushing"
                    },
                    {
                        "id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1",
                        "name": "Harrison Ford"
                    },
                    {
                        "id": "26e83050-29ef-4163-a99d-b546cac208f8",
                        "name": "Mark Hamill"
                    }
                ],
                "writers": [
                    {
                        "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
                        "name": "George Lucas"
                    }
                ]
            }
        }


class PopularShortFilm(ShortFilm):
    _index: IndexType = IndexType.MOVIES

    @classmethod
    def fill_elk(cls, data):
        if 'top_rated_films' not in data \
                or 'hits' not in data['top_rated_films'] \
                or 'hits' not in data['top_rated_films']['hits'] \
                or len(data['top_rated_films']['hits']['hits']) == 0 \
                or '_source' not in data['top_rated_films']['hits']['hits'][0]:
            return None

        return cls(**data['top_rated_films']['hits']['hits'][0]['_source'])


class PopularShortFilms(ShortFilms):
    __model__: PopularShortFilm = PopularShortFilm

    @classmethod
    def fill_elk(cls, data):
        if 'aggregations' not in data \
                or 'themes' not in data['aggregations'] \
                or 'buckets' not in data['aggregations']['themes']:
            return None

        model = cls()
        model.__root__ = [cls.__model__.fill_elk(i) for i in data['aggregations']['themes']['buckets']]

        return model
