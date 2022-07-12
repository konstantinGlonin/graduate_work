from fastapi.params import Query

from core.locales import _
from models.params import FilterField, Filters


def film_filter_params(
        title: str | None = Query(
            None,
            title=_("Поиск по наименованию фильма"),
            description=_("Поиск по наименованию фильма"),
            alias="query",
        ),
        genres: str | None = Query(
            None,
            title=_("Фильтрация по жанру"),
            description=_("Фильтрация по жанру, в качестве параметра передается ID"),
            alias="filter[genres_id]",
        ),
        actors: str | None = Query(
            None,
            title=_("Фильтрация по актеру"),
            description=_("Фильтрация по актеру, в качестве параметра передается ID."),
            alias="filter[actors_id]",
        ),
        director: str | None = Query(
            None,
            title=_("Фильтрация по режиссеру"),
            description=_("Фильтрация по режиссеру, в качестве параметра передается ID."),
            alias="filter[director_id]",
        ),
        writers: str | None = Query(
            None,
            title=_("Фильтрация по сценаристу"),
            description=_("Фильтрация по сценаристу, в качестве параметра передается ID."),
            alias="filter[writers_id]",
        ),
        person: str | None = Query(
            None,
            title=_("Фильтрация по персоне"),
            description=_("Фильтрация по персоне не зависимо от роли, в качестве параметра передается ID."),
            alias="filter[persons_id]",
        )
):
    film_filters = Filters()
    if title is not None:
        film_filters.add(FilterField(field='title', val=title))

    if genres is not None:
        film_filters.add(FilterField(field='genres_id', val=genres))

    if actors is not None:
        film_filters.add(FilterField(field='actors_id', val=actors))

    if director is not None:
        film_filters.add(FilterField(field='director_id', val=director))

    if writers is not None:
        film_filters.add(FilterField(field='writers_id', val=writers))

    if person is not None:
        film_filters.add(FilterField(field='persons_id', val=person))

    return film_filters


def genre_filter_parameter(
        name_search: str | None = Query(
            None,
            title=_("Фильтрация по названию жанра"),
            description=_("Фильтрация по названию жанра, в качестве параметра передается название жанра."),
            alias="query",
        ),
        description_search: str | None = Query(
            None,
            title=_("Фильтрация по описанию жарна"),
            description=_("Фильтрация по описанию жарна"),
            alias="description",
        ),
):
    genre_filters = Filters()

    if name_search is not None:
        genre_filters.add(FilterField(field='name.ngr', val=name_search))
    if description_search is not None:
        genre_filters.add(FilterField(field='description.ngr', val=description_search))

    return genre_filters


def person_filter_parameter(

        name: str | None = Query(
            None,
            title=_("Фильтрация по имени персоны"),
            description=_("Фильтрация по имени персоны, в качестве параметра передается имя."),
            alias="query",
        ),
        film_id: str | None = Query(
            None,
            title=_("Фильтрация по фильму"),
            description=_("Фильтрация по фильму, в качестве параметра передается ID."),
            alias="filter[film_id]",
        )
):
    person_filters = Filters()

    if name is not None:
        person_filters.add(FilterField(field='name.ngr', val=name))
    if film_id is not None:
        person_filters.add(FilterField(field='film_ids', val=film_id))

    return person_filters
