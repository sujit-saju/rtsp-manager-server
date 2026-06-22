import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename

UPLOAD_ROOT = Path("uploads")
VIDEO_DIR = UPLOAD_ROOT / "videos"

ALLOWED_EXTENSIONS = {
    "mp4",
    "avi",
    "mov",
    "mkv",
    "flv",
    "webm",
}


def allowed_file(filename: str):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


async def upload_video(file):
    if file is None:
        raise ValueError("No file provided")

    if file.filename == "":
        raise ValueError("Filename is empty")

    if not allowed_file(file.filename):
        raise ValueError("Unsupported file format")

    # Create uploads/videos directory if not exists
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    filename = secure_filename(file.filename)

    destination = VIDEO_DIR / filename

    # Generate unique name if file already exists
    if destination.exists():
        ext = destination.suffix
        name = destination.stem
        filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        destination = VIDEO_DIR / filename

    await file.save(destination)

    # Return relative path
    return str(destination).replace("\\", "/")