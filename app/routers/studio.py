from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.database import SessionDep
from app.models import Studio
from app.schema.studio import StudioCreate, StudioPublic

studio_router = APIRouter(prefix='/studios', tags=['studios'])


def get_studio_or_404(session: SessionDep, studio_id: int) -> Studio:
    studio = session.get(Studio, studio_id)
    if studio is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Estúdio não encontrado.'
        )
    return studio


@studio_router.post('/', status_code=HTTPStatus.CREATED, response_model=StudioPublic)
def create_studio(studio: StudioCreate, session: SessionDep):
    db_studio = Studio(**studio.model_dump())
    session.add(db_studio)
    session.commit()
    session.refresh(db_studio)
    return db_studio


@studio_router.get('/{studio_id}', response_model=StudioPublic)
def read_studio(studio_id: int, session: SessionDep):
    return get_studio_or_404(session, studio_id)