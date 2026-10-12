from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.database import SessionDep
from app.models import Author
from app.schema.author import AuthorCreate, AuthorPublic

author_router = APIRouter(prefix='/authors', tags=['authors'])


def get_author_or_404(session: SessionDep, author_id: int) -> Author:
    author = session.get(Author, author_id)
    if author is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Autor não encontrado.'
        )
    return author


@author_router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
def create_author(author: AuthorCreate, session: SessionDep):
    db_author = Author(**author.model_dump())
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@author_router.get('/{author_id}', response_model=AuthorPublic)
def read_author(author_id: int, session: SessionDep):
    return get_author_or_404(session, author_id)