from fastapi import APIRouter

from api.v1.recommendations import router as recommendations_router

router = APIRouter(prefix="/v1")
router.include_router(recommendations_router)
