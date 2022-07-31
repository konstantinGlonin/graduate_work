import csv

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse

from api import router as api_router
from core import services

ROUTERS = (api_router,)


def prepare_app(routers: tuple[APIRouter]) -> FastAPI:
    """Init app, app routes etc."""

    fastapi_app = FastAPI(
        title="data service api",
        docs_url="/ugc/api/openapi",
        openapi_url="/ugc/api/openapi.json",
        default_response_class=ORJSONResponse,
    )
    for router in routers:
        fastapi_app.include_router(router)
    return fastapi_app


app = prepare_app(ROUTERS)

ratings = {}


@app.on_event("startup")
async def startup() -> None:
    """Startup hook."""
    services.DB = services.SampleDB()
    services.DB.load_data()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown hook."""
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
