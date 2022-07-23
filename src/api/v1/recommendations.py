from fastapi import APIRouter, Depends

from core.services import (get_mongo_client,
                           get_rabbit_connection,
                           get_top,
                           put_request_on_new_recommendation_into_queue,
                           user_recommendation)
from models.recomendations import BaseRecommendations

router = APIRouter(prefix="/recommendation", tags=["recommendation"])


@router.post("/user")
async def user_recommendation(data: BaseRecommendations,
                              recommendation=Depends(user_recommendation),
                              rabbit=Depends(get_rabbit_connection)):
    if recommendation:
        return {"recommendations": recommendation}

    await put_request_on_new_recommendation_into_queue(data=data, rabbit=rabbit)

    top = await get_top()
    return {"top_20": top}


@router.post("/movie")
async def movie_recommendation(movie_id: BaseRecommendations,
                               mongo=Depends(get_mongo_client)):
    coll = mongo.movies.collection_name
    return "hello"
