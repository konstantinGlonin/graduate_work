from fastapi import APIRouter

from api.v1.data_service import router as data_service_router

router = APIRouter(prefix="/v1")
router.include_router(data_service_router)
