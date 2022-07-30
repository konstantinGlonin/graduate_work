from datetime import datetime
from typing import Any, Union
from uuid import UUID

import orjson
from pydantic import BaseModel, Field

from core.config import Config


def orjson_dumps(value: Union[list, dict], *, default: Union[list, dict]) -> Any:
    return orjson.dumps(value, default=default).decode()


class BaseOrJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseRecommendations(BaseOrJSONModel):
    id: UUID
    type: str


class Recommendation(BaseRecommendations):
    id: UUID
    type: str
    data: list = []
    model_version: str = Field(default_factory=Config().get_model_version)
    updated_at: datetime = Field(default_factory=datetime.now)
    counter: int = 0

    def safe_dict(self):
        data = self.dict()
        data["id"] = str(self.id)
        return data
