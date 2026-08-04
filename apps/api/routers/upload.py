import io
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile, status
from PIL import Image, UnidentifiedImageError

from config import (
    ALLOWED_IMAGE_TYPES,
    MAX_FILE_SIZE,
    MAX_FILE_SIZE_MB,
    MIN_IMAGE_DIMENSION,
    UPLOAD_DIR,
)
from schemas import APIError, ErrorCode, ErrorResponse, PhotoRole, UploadResponse

router = APIRouter()

FileField = Annotated[UploadFile, File(description="Photo file (jpeg/png/webp)")]
RoleField = Annotated[PhotoRole, Form(description="Who is on the photo")]


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file type or image"},
        413: {"model": ErrorResponse, "description": "File too large"},
    },
)
async def upload(file: FileField, role: RoleField) -> UploadResponse:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise APIError(
            400,
            ErrorCode.invalid_file_type,
            f"unsupported content type: {file.content_type}",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise APIError(
            413,
            ErrorCode.file_too_large,
            f"max {MAX_FILE_SIZE_MB} MB",
        )

    try:
        with Image.open(io.BytesIO(content)) as img:
            img.verify()
        with Image.open(io.BytesIO(content)) as img:
            img.load()
            width, height = img.size
        if width < MIN_IMAGE_DIMENSION or height < MIN_IMAGE_DIMENSION:
            raise APIError(
                400,
                ErrorCode.image_too_small,
                f"min {MIN_IMAGE_DIMENSION}x{MIN_IMAGE_DIMENSION}, got {width}x{height}",
            )
    except UnidentifiedImageError:
        raise APIError(400, ErrorCode.invalid_image, "file is not a valid image") from None
    except OSError as exc:
        raise APIError(400, ErrorCode.invalid_image, f"cannot read image: {exc}") from None
    except Image.DecompressionBombError:
        raise APIError(400, ErrorCode.invalid_image, "image dimensions too large") from None

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename or "image.jpg").suffix or ".jpg"
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{ext}"
    (UPLOAD_DIR / filename).write_bytes(content)
    return UploadResponse(file_id=file_id, filename=filename, role=role)
