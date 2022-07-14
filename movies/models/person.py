from uuid import UUID

from models.mixin import IndexType, ListMixin, ModelMixin


class ShortPerson(ModelMixin):
    _index: IndexType = IndexType.PERSON

    id: UUID
    name: str


class ShortFilm(ModelMixin):
    _index: IndexType = IndexType.MOVIES

    id: UUID
    title: str


class Person(ShortPerson):
    actor: list[ShortFilm] = None
    writer: list[ShortFilm] = None
    director: list[ShortFilm] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "1989ed1e-0c0b-4872-9dfb-f5ed13c764e2",
                "name": "Irvin Kershner",
                "actor": [
                    {
                        "id": "a2ff04cc-eede-43fc-a503-07f037be8cc8",
                        "title": "Star Wars: Music by John Williams"
                    }
                ],
                "writer": 'null',
                "director": [
                    {
                        "id": "4f53452f-a402-4a76-89fd-f034eeb8d657",
                        "title": "Star Wars: Episode V - The Empire Strikes Back: Deleted Scenes"
                    },
                    {
                        "id": "0312ed51-8833-413f-bff5-0e139c11264a",
                        "title": "Star Wars: Episode V - The Empire Strikes Back"
                    }
                ]
            }
        }


class ShortPersons(ListMixin):
    __model__: ShortPerson = ShortPerson
    __root__: list[ShortPerson] = []

    class Config:
        schema_extra = {
            "example": [
                {
                    "id": "1989ed1e-0c0b-4872-9dfb-f5ed13c764e2",
                    "name": "Irvin Kershner"
                }
            ]
        }
