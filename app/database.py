from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy.orm import sessionmaker

from app.settings import Settings

engine = create_engine(Settings().DATABASE_URL)
Session = sessionmaker(bind=engine, autoflush=False)


def get_session() -> Generator[OrmSession, None, None]:
    with Session() as session:
        yield session


SessionDep = Annotated[OrmSession, Depends(get_session)]
