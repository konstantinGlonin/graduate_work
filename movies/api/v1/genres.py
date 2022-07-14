from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.v1.params.params import genre_params, ParamsGrp
from core.locales import _
from models.genre import Genre, Genres
from services.base import Service, get_service

router = APIRouter()


@router.get('',
            response_model=Genres,
            summary="Поиск/фильтрация по жанрам",
            description=
            """
            Выбирает в хранилище жанры в соответствии с переданными фильтрами.
            Выводит в соответствии с переданными параметрами сортировки и пагинации.
            В случае пустого результата выводит 'genres not found'
            Если ни одного фильтра/сортировки не передано, отдает все жанры по 50 записей на страницу.
            """
            )
async def genre_filter(
        params: ParamsGrp = Depends(genre_params),
        service: Service = Depends(get_service)
) -> Genres:
    data = await service.search(params, Genres)

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=_('genres not found'))

    return data


@router.get('/{genre_id}',
            response_model=Genre,
            summary="Полная информация о жанре",
            description=
            """
            Выбирает в хранилище жанр по данному ID.
            Если запись найдена, возвращает полную информацию о жанре.
            В противном случае 'genre not found'
            """
            )
async def genre_details(
        genre_id: UUID,
        service: Service = Depends(get_service)
) -> Genre:
    data = await service.get(genre_id, Genre)
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=_('genre not found'))

    return data
