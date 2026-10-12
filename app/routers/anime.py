from http import HTTPStatus

from fastapi import APIRouter, HTTPException, UploadFile

from app.database import SessionDep
from app.models import Anime
from app.schema.anime import AnimeCover, AnimeCreate, AnimePublic
from app.utils.files import delete_cover, read_and_validate_image, save_cover

anime_router = APIRouter(prefix='/anime', tags=['animes'])


def get_anime_or_404(session: SessionDep, anime_id: int) -> Anime:
    anime = session.get(Anime, anime_id)
    if anime is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Anime não encontrado.'
        )
    return anime


@anime_router.post('/', status_code=HTTPStatus.CREATED, response_model=AnimePublic)
def create_anime(anime: AnimeCreate, session: SessionDep):
    db_anime = Anime(**anime.model_dump())
    session.add(db_anime)
    session.commit()
    session.refresh(db_anime)
    return db_anime


@anime_router.get('/{anime_id}', response_model=AnimePublic)
def read_anime(anime_id: int, session: SessionDep):
    return get_anime_or_404(session, anime_id)


# ---------- Obrigatório: upload da capa ----------
@anime_router.post('/{anime_id}/cover', response_model=AnimeCover)
def upload_cover(anime_id: int, cover_file: UploadFile, session: SessionDep):
    anime = get_anime_or_404(session, anime_id)

    content, extension = read_and_validate_image(cover_file)

    old_cover = anime.cover
    new_cover = save_cover(anime_id, content, extension)
    anime.cover = new_cover

    try:
        session.commit()
    except Exception:
        session.rollback()
        delete_cover(new_cover)  # não deixa arquivo órfão
        raise

    delete_cover(old_cover)  # só depois do commit
    session.refresh(anime)
    return {'cover': anime.cover}


# ---------- Desafio: DELETE da capa ----------
@anime_router.delete('/{anime_id}/cover', status_code=HTTPStatus.NO_CONTENT)
def remove_cover(anime_id: int, session: SessionDep):
    anime = get_anime_or_404(session, anime_id)

    if anime.cover is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Este anime não possui capa.',
        )

    old_cover = anime.cover
    anime.cover = None
    session.commit()
    delete_cover(old_cover)  # só depois do commit


# ---------- Intermediário: delete_anime apagando a capa ----------
@anime_router.delete('/{anime_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_anime(anime_id: int, session: SessionDep):
    anime = get_anime_or_404(session, anime_id)

    old_cover = anime.cover
    session.delete(anime)
    session.commit()
    delete_cover(old_cover)  # só depois do commit
