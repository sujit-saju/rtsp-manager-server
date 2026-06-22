import os

from quart import Blueprint, request
from app.core.config import Config
from app.core.session import get_db
from app.services.stream_service import StreamService
from quart_schema import validate_querystring, validate_request, validate_response, tag

from app.utils.file_upload import upload_video
from app.utils.stream_utils import CreateStreamRequest

API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
stream_bp = Blueprint("stream", __name__, url_prefix=f"{API_PREFIX}/cameras")


class StreamController:

    def __init__(self):
        self.bp = Blueprint(
            "stream",
            __name__,
            url_prefix=f"{Config.API_PREFIX}/stream",
        )

        self.register_routes()

    def register_routes(self):

        self.bp.add_url_rule(
            "/add",
            view_func=self.create_stream,
            methods=["POST"],
        )

        self.bp.add_url_rule(
            "",
            view_func=self.get_all_streams,
            methods=["GET"],
        )

        self.bp.add_url_rule(
            "/<string:uniq_code>",
            view_func=self.get_stream,
            methods=["GET"],
        )

        self.bp.add_url_rule(
            "/<string:uniq_code>",
            view_func=self.update_stream,
            methods=["PUT"],
        )

        self.bp.add_url_rule(
            "/<string:uniq_code>",
            view_func=self.delete_stream,
            methods=["DELETE"],
        )

        self.bp.add_url_rule(
            "/upload", view_func=self.upload_video_for_streaming, methods=["POST"]
        )

    @tag(["Stream"])
    @validate_request(CreateStreamRequest)
    async def create_stream(self, stream_data: CreateStreamRequest):
        """
        Create streams
        """
        async with get_db() as db:
            service = StreamService(db)

        response, status_code = await service.create_stream(stream_data)

        return response, status_code

    async def get_all_streams(self):
        return await self.service.get_all_streams()

    async def get_stream(self, uniq_code):
        return await self.service.get_stream(uniq_code)

    async def update_stream(self, uniq_code):
        data = await request.get_json()
        data["uniqCode"] = uniq_code
        return await self.service.update_stream(data)

    async def delete_stream(self, uniq_code):
        return await self.service.delete_stream(uniq_code)

    @tag(["Stream"])
    async def upload_video_for_streaming(self):
        # Read uploaded files
        files = await request.files
        file = files["file"]
        try:
            file_path = await upload_video(file)

            return {
                "success": True,
                "message": "Video uploaded successfully.",
                "path": file_path,
            }, 200

        except Exception as ex:
            import traceback

            traceback.print_exc()

            return {"success": False, "message": str(ex)}, 500

    @classmethod
    def blueprint(cls):

        return cls().bp
