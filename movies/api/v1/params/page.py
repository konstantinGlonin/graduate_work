from fastapi.params import Query

from core.locales import _
from models.params import Page


def page_params(
        number: int | None = Query(
            1,
            title=_("Номер страницы"),
            description=_("Номер страницы"),
            alias="page[number]",
            ge=1
        ),
        size: int | None = Query(
            50,
            title=_("Кол-во результатов на странице"),
            description=_("Кол-во результатов на странице"),
            alias="page[size]",
            ge=1,
            lt=1000
        )
) -> Page:
    return Page(number=number, size=size)
