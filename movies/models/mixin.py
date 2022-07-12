from enum import Enum
from typing import Any

import orjson as orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class IndexType(Enum):
    MOVIES = 'movies'
    PERSON = 'person'
    GENRE = 'genre'


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ModelMixin(BaseOrjsonModel):
    _index: IndexType = IndexType.MOVIES

    @classmethod
    def fill_elk(cls, data):
        if '_source' not in data:
            return None
        return cls(**data['_source'])

    @classmethod
    def get_index(cls):
        return cls._index.value


class ListMixin(BaseOrjsonModel):
    __model__: ModelMixin = ModelMixin
    __root__: list[ModelMixin] = []

    def get_index(self):
        return self.__model__.get_index()

    @classmethod
    def fill_elk(cls, data):
        if 'hits' not in data and 'hits' not in data['hits']:
            return None

        model = cls()
        model.__root__ = [cls.__model__.fill_elk(i) for i in data['hits']['hits']]

        return model


class MixinParamsField(BaseModel):
    field: str
    val: Any

    def value(self):
        return self.val

    def to_elk(self):
        return {self.field: self.value()}

    def rhash(self, sep=':'):
        return f'{self.field}{sep}{self.val}'


class MixinParams(BaseModel):
    __root__: list[MixinParamsField] = []

    def __len__(self):
        return len(self.__root__)

    def add(self, obj: MixinParamsField):
        self.__root__.append(obj)

    def rhash(self, sep='::'):
        return f'{sep}'.join([i.rhash() for i in self.__root__])

    def to_elk(self):
        return [i.to_elk() for i in self.__root__]


class MixinParamsGrp(BaseModel):
    index: IndexType = IndexType.MOVIES
    body: dict | None = None

    def rhash(self, sep=':::'):
        return self.index.value

    def hash(self, sep=':::'):
        return self.index.value

    def to_elk(self):
        pass
