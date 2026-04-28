import os
import shutil
from uuid import uuid4
from fastapi import UploadFile, HTTPException

from app.config import get_settings


settings = get_settings()


ALLOWED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg"]


def validate_file(file: UploadFile):
    filename = file.filename.lower()

    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG, and JPEG files are supported."
        )


async def save_upload_file(file: UploadFile) -> str:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path