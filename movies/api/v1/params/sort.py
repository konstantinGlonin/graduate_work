from fastapi.params import Query

from core.locales import _
from models.params import Sort


def sort_params(
        sort: str | None = Query(
            "-_score",
            title=_("Сортировка по полям"),
            description=_("Сортировка по полям список полей через запятую в формате -field для сортировки по" \
                          " убыванию или field для сортировки по возрастанию"),
            alias="sort",
        ),
) -> Sort:

    return Sort.parse(sort)
