from enum import StrEnum

from fastapi import HTTPException
from pydantic import BaseModel


class PhotoRole(StrEnum):
    mom = "MOM"
    dad = "DAD"
    baby = "BABY"


class ErrorCode(StrEnum):
    invalid_file_type = "invalid_file_type"
    file_too_large = "file_too_large"
    invalid_image = "invalid_image"
    image_too_small = "image_too_small"


class HealthResponse(BaseModel):
    status: str


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    role: PhotoRole


class ErrorResponse(BaseModel):
    code: ErrorCode
    detail: str


class APIError(HTTPException):
    def __init__(self, status_code: int, code: ErrorCode, detail: str) -> None:
        super().__init__(
            status_code=status_code,
            detail=ErrorResponse(code=code, detail=detail).model_dump(),
        )

