import json

from aio_pika import Message
from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse

from core.services import get_mongo_client
from models.recomendations import BaseRecommendations


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/")
async def get_recommendation(mongo=Depends(get_mongo_client)):
    coll = mongo.movies.collection_name
    return "hello"
