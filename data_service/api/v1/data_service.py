from fastapi import APIRouter

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/get")
async def get_recommendation():
    return "hello"
