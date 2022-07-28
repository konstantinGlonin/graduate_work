import aio_pika
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from api import router as api_router
from core import services
from core.config import Config

ROUTERS = (api_router,)

config = Config()


def prepare_app(routers: tuple[APIRouter]) -> FastAPI:
    """Init app, app routes etc."""

    fastapi_app = FastAPI(
        title="recommendations api",
        docs_url="/recommendations/api/openapi",
        openapi_url="/recommendations/api/openapi.json",
        default_response_class=ORJSONResponse,
    )
    for router in routers:
        fastapi_app.include_router(router)
    return fastapi_app


app = prepare_app(ROUTERS)


@app.on_event("startup")
async def startup() -> None:
    """Startup hook."""
    services.MONGO_CLIENT = AsyncIOMotorClient(config.mongo.host, config.mongo.port)
    services.RABBIT_CONNECTION = await aio_pika.connect(
        host=config.rabbit.host,
        port=config.rabbit.port,
        password=config.rabbit.password,
        login=config.rabbit.username
    )


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown hook."""
    await services.RABBIT_CONNECTION.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        debug=True
    )
