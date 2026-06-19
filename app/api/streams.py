
from quart import Blueprint, request, jsonify
from uuid import uuid4
from pathlib import Path

streams_bp=Blueprint("streams",__name__)
UPLOAD_DIR=Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@streams_bp.post("/upload")
async def upload():
    files=await request.files
    if "file" not in files:
        return jsonify({"success":False,"message":"No file uploaded"}),400
    file=files["file"]
    ext=Path(file.filename).suffix
    code=f"STRM{uuid4().hex[:8].upper()}"
    save_path=UPLOAD_DIR/f"{code}{ext}"
    await file.save(save_path)
    return jsonify({
        "success":True,
        "streamCode":code,
        "streamUrl":f"rtsp://<server-ip>:8554/{code}",
        "status":"PENDING",
        "filePath":str(save_path)
    })

@streams_bp.get("")
async def list_streams():
    return jsonify([])

@streams_bp.post("/<stream_code>/start")
async def start(stream_code):
    return jsonify({"streamCode":stream_code,"status":"RUNNING"})

@streams_bp.post("/<stream_code>/stop")
async def stop(stream_code):
    return jsonify({"streamCode":stream_code,"status":"STOPPED"})

@streams_bp.delete("/<stream_code>")
async def delete(stream_code):
    return jsonify({"deleted":stream_code})
