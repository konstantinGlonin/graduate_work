from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.v1.params.params import person_params, ParamsGrp
from core.locales import _
from models.mixin import IndexType
from models.person import Person, ShortPersons
from services.base import Service, get_service


router = APIRouter()


@router.get('',
            response_model=ShortPersons,
            summary="Поиск/фильтрация по персонам",
            description=
            """
            Выбирает в хранилище персон в соответствии с переданными фильтрами.
            Выводит в соответствии с переданными параметрами сортировки и пагинации.
            В случае пустого результата выводит 'persons not found'
            Если ни одного фильтра/сортировки не передано, отдает все персоны по 50 записей на страницу.
            """
            )
async def person_filter(
        params: ParamsGrp = Depends(person_params),
        service: Service = Depends(get_service)
) -> ShortPersons:
    data = await service.search(params, ShortPersons)

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=_('persons not found'))

    return data


@router.get('/{person_id}',
            response_model=Person,
            summary="Полная информация о персоне",
            description=
            """
            Выбирает в хранилище персону по данному ID.
            Если запись найдена, возвращает полную информацию о персоне.
            В противном случае 'person not found'
            """
            )
async def person_details(
        person_id: UUID,
        service: Service = Depends(get_service)
) -> Person:
    data = await service.get(person_id, Person)

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=_('person not found'))

    return data
