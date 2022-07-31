from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from core.services import get_db, SampleDB

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/get_user_films/{movie_id}",
            response_model=List[UUID],
            summary="Список фильмов просмотренных пользователем",
            description="""
            Возвращает список фильмов рекомендованных конкретному фильму.
            """
            )
def get_films(movie_id: UUID = "f0c3cebe-1032-11ed-84a8-e1444c900301", db: SampleDB = Depends(get_db)):
    film_list = db.get(movie_id)
    if film_list:
        return db.get(str(movie_id))
    raise HTTPException(status_code=404, detail="Item not found")
