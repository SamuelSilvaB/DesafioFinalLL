from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import table_registry

if TYPE_CHECKING:
    from app.models.anime import Anime


@table_registry.mapped_as_dataclass
class Studio:
    __tablename__ = 'studio'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), init=False
    )

    animes: Mapped[list['Anime']] = relationship(
        back_populates='studio', default_factory=list, init=False
    )