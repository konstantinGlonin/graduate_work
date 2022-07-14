from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.v1.params.params import film_params, popular_film_params
from core.locales import _
from models.films import Film, ShortFilms, PopularShortFilms
from models.mixin import MixinParamsGrp
from services.base import Service, get_service

router = APIRouter()


@router.get('',
            response_model=ShortFilms,
            summary="Поиск/фильтрация по кинопроизведениям",
            description=
            """
            Выбирает в хранилище кинопроизведения в соответствии с переданными фильтрами.
            Выводит в соответствии с переданными параметрами сортировки и пагинации.
            В случае пустого результата выводит 'films not found'
            Если ни одного фильтра/сортировки не передано, отдает все кинопроизведения по 50 записей на страницу.
            Информация о кинопроизведении выводится в сокращенном виде:
            id: uuid
            title: str
            imdb_rating: float
            """)
async def film_filter(
        params: MixinParamsGrp = Depends(film_params),
        service: Service = Depends(get_service)
) -> ShortFilms:
    data = await service.search(params, ShortFilms)

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=_('films not found'))

    return data


@router.get('/{film_id}',
            response_model=Film,
            summary="Полная информация о кинопроизведении",
            description=
            """
            Выбирает в хранилище кинопроизведение по данному ID.
            Если запись найдена, возвращает полную информацию о кинопроизведении.
            В противном случае 'film not found'
            """)
async def film_details(
        film_id: UUID,
        service: Service = Depends(get_service),
) -> Film:
    data = await service.get(film_id, Film)
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=_('film not found'))

    return data


@router.get('_popular',
            response_model=PopularShortFilms,
            summary="Популярные кинопроизведения",
            description=
            """
            Выбирает в хранилище 20 самых популярных кинопроизведений основываясь на их жанре/жанрах
            """)
async def film_popular(
        params: MixinParamsGrp = Depends(popular_film_params),
        service: Service = Depends(get_service)
) -> PopularShortFilms:
    data = await service.search(params, PopularShortFilms)
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=_('films not found'))

    return data
