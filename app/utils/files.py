import uuid
from http import HTTPStatus
from pathlib import Path

from fastapi import HTTPException, UploadFile

BASE_DIR = Path(__file__).resolve().parents[2]
COVERS_FOLDER = BASE_DIR / 'static' / 'covers'
COVERS_URL = '/static/covers'

ALLOWED_FILE_TYPES = {
    'image/png': '.png',
    'image/jpeg': '.jpg',
    'image/webp': '.webp',
}
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024


def detect_image_type(data: bytes) -> str | None:
    """Descobre o tipo real da imagem pelos magic bytes."""
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    if data.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'image/webp'
    return None


def read_and_validate_image(file: UploadFile) -> tuple[bytes, str]:
    """Devolve (conteúdo, extensão) ou levanta HTTPException."""
    content = file.file.read(MAX_FILE_SIZE + 1)
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            detail=f'O arquivo é maior que {MAX_FILE_SIZE_MB} MB.',
        )

    real_type = detect_image_type(content)
    if real_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            detail=(
                'Formato de imagem não suportado. '
                f'Formatos permitidos: {",".join(sorted(ALLOWED_FILE_TYPES))}'
            ),
        )
    return content, ALLOWED_FILE_TYPES[real_type]


def save_cover(anime_id: int, content: bytes, extension: str) -> str:
    """Salva a imagem no disco e devolve a URL pública."""
    COVERS_FOLDER.mkdir(parents=True, exist_ok=True)
    file_name = f'{anime_id}_{uuid.uuid4().hex}{extension}'
    (COVERS_FOLDER / file_name).write_bytes(content)
    return f'{COVERS_URL}/{file_name}'


def delete_cover(cover_url: str | None) -> None:
    """Apaga a imagem do disco a partir da URL guardada no banco."""
    if cover_url:
        (COVERS_FOLDER / Path(cover_url).name).unlink(missing_ok=True)
