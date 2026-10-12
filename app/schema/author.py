from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    name: str = Field(..., max_length=150)


class AuthorCreate(AuthorBase):
    pass


class AuthorPublic(AuthorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)