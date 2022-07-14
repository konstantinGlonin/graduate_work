from uuid import UUID

from models.mixin import IndexType, ListMixin, ModelMixin


class ShortGenre(ModelMixin):
    _index = IndexType.GENRE
    id: UUID
    name: str


class Genre(ShortGenre):
    description: str = None

    class Config:
        schema_extra = {
            "example": {
                "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                "name": "Action",
                "description": 'null'
            }
        }


class Genres(ListMixin):
    __model__: Genre = Genre
    __root__: list[Genre] = []

    class Config:
        schema_extra = {
            "example": [
                {
                    "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                    "name": "Action",
                    "description": 'null'
                }
            ]
        }
