from uuid import UUID

from fastapi import APIRouter, Depends

from core.services import (get_mongo_client,
                           get_rabbit_connection,
                           get_top,
                           put_request_on_new_recommendation_into_queue,
                           get_recommendation)
from domain.recomendations import BaseRecommendations

router = APIRouter(prefix="/recommendation", tags=["recommendation"])


@router.get("/user/{user_id}",
            response_model=list[str, str],
            summary="Рекомендация для пользователя",
            description="""
            Возвращает список фильмов рекомендованных конкретному пользователю.
            """
            )
async def user_recommendation(user_id: UUID,
                              mongo=Depends(get_mongo_client),
                              rabbit=Depends(get_rabbit_connection)):
    data = BaseRecommendations(**{"id": user_id, "type": "user"})
    recommendation = await get_recommendation(data=data, mongo=mongo, rabbit=rabbit)

    if recommendation:
        return recommendation

    await put_request_on_new_recommendation_into_queue(data=data, rabbit=rabbit)

    top = await get_top()
    return top


@router.get("/movie/{movie_id}",
            response_model=list,
            summary="Рекомендация для фильма",
            description="""
            Возвращает список фильмов рекомендованных конкретному фильму.
            """
            )
async def movie_recommendation(movie_id: UUID,
                               mongo=Depends(get_mongo_client),
                               rabbit=Depends(get_rabbit_connection)):
    data = BaseRecommendations(**{"id": movie_id, "type": "movie"})
    recommendation = await get_recommendation(data=data, mongo=mongo, rabbit=rabbit)

    if recommendation:
        return recommendation

    await put_request_on_new_recommendation_into_queue(data=data, rabbit=rabbit)

    top = await get_top()
    return top
