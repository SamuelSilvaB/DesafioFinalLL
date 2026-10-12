from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StudioBase(BaseModel):
    name: str = Field(..., max_length=150)


class StudioCreate(StudioBase):
    pass


class StudioPublic(StudioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)