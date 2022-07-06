from uuid import UUID

from pydantic import BaseModel


class BaseRecommendations(BaseModel):
    id: UUID
