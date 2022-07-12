import hashlib
from enum import Enum

from pydantic import BaseModel

from models.mixin import MixinParamsField, MixinParams
from models.mixin import MixinParamsGrp


class Order(str, Enum):
    DESC = 'desc'
    ASC = 'asc'


class FilterField(MixinParamsField):
    pass


class Filters(MixinParams):

    def to_elk(self):
        if len(self) == 0:
            return {
                "match_all": {}
            }

        return {
            "bool": {
                "must": [
                    {"match": i.to_elk()} for i in self.__root__
                ]
            }
        }


class OrderField(MixinParamsField):

    def value(self):
        return self.val.value

    @classmethod
    def parse(cls, field: str = None):
        if field and type(field) == str:
            order = Order.ASC

            if '-' == field[0]:
                order = Order.DESC
                field = field[1:]

            if order is not None and field is not None:
                return cls(field=field, val=order)

        return None


class Sort(MixinParams):

    @classmethod
    def parse(cls, sort):
        fields = [sort]
        if ',' in sort:
            fields = sort.split(',')

        return cls(__root__=[i for i in [OrderField.parse(sort) for sort in fields] if i is not None])


class Page(BaseModel):
    number: int = 1
    size: int = 50

    def rhash(self, sep=':'):
        return f'{self.number}{sep}{self.size}'

    def offset(self):
        return self.size * (self.number - 1)


class BaseParamsGrp(MixinParamsGrp):

    def to_elk(self):
        query = {
            'index': self.index.value,
        }

        if self.body is not None:
            query['body'] = self.body

        return query


class ParamsGrp(MixinParamsGrp):
    filters: Filters | None = None
    sort: Sort | None = None
    page: Page | None = None

    def rhash(self, sep=':::'):

        return f'{sep}'.join([self.index.value, self.filters.rhash(), self.sort.rhash(), self.page.rhash()])

    def hash(self, sep=':::'):

        return hashlib.md5(str(self.json()).encode('utf-8')).hexdigest()

    def to_elk(self):
        query = {
            'index': self.index.value,
        }

        if self.page is not None:
            query['size'] = self.page.size
            query['from_'] = self.page.offset()

        if self.filters is not None and len(self.filters) > 0:
            query['query'] = self.filters.to_elk()

        if self.sort is not None and len(self.sort) > 0:
            query['sort'] = self.sort.to_elk()

        return query
