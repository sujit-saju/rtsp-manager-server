import uuid
import cv2
from pathlib import Path
from werkzeug.utils import secure_filename

VIDEO_DIR = Path("uploads/videos")
SNAPSHOT_DIR = Path("uploads/snapshots")

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

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    filename = secure_filename(file.filename)
    destination = VIDEO_DIR / filename

    # Generate unique name if file already exists
    if destination.exists():
        ext = destination.suffix
        name = destination.stem
        filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        destination = VIDEO_DIR / filename

    await file.save(destination)

    # Create snapshot
    snapshot_filename = f"{destination.stem}.jpg"
    snapshot_path = SNAPSHOT_DIR / snapshot_filename

    cap = cv2.VideoCapture(str(destination))

    # Optional: jump to 1 second into the video
    cap.set(cv2.CAP_PROP_POS_MSEC, 1000)

    success, frame = cap.read()
    cap.release()

    if success:
        cv2.imwrite(str(snapshot_path), frame)
    else:
        snapshot_path = None

    return {
        "video_path": str(destination).replace("\\", "/"),
        "snapshot_path": (
            str(snapshot_path).replace("\\", "/")
            if snapshot_path
            else None
        ),
    }