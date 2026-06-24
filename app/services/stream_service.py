from app.models.stream_entity import Stream
from app.repositories.stream_repository import StreamRepository
from app.utils.response import success_response, error_response
from app.services.unique_code_service import UniqueCodeService

import threading

from app.utils.stream_manager import get_rtsp_url, starting_streaming

class StreamService:

    def __init__(self, db):
        self.db = db
        self.stream_repo = StreamRepository(db)
        self.unique_code_service = UniqueCodeService(db)

    async def create_stream(self, data):

        existing = await self.stream_repo.find_by_stream_name(data.streamName)

        if existing:
            return (
                error_response("Stream already exists."),
                409,
            )

        uniq_code = await self.unique_code_service.generate("STREAM")

        new_stream = Stream(
            uniq_code=uniq_code,
            stream_name=data.streamName,
            file_path=data.filePath,
            fps=data.fps,
            resolution=data.resolution,
            loop_enabled=data.loopEnabled,
            status=data.status,
            snapshot_path=data.snapshotPath,
        )

        stream = await self.stream_repo.create(new_stream)

        # After stream is saved:
        rtsp_url = starting_streaming(stream)
        
        return (
            success_response(
                "Stream created successfully.",
                {
                    "streamName": stream.stream_name,
                    "fps": stream.fps,
                    "uniqCode": uniq_code,
                    "resolution": stream.resolution,
                    "status": stream.status,
                    "loopEnabled": stream.loop_enabled,
                    "snapshotPath": stream.snapshot_path,
                    "rtspUrl": rtsp_url
                },
            ),
            201,
        )

    async def list_all_streams(self):
        stream_list = await self.stream_repo.get_all_streams()

        stream_data = [
            {
                "id": stream.id,
                "uniqCode": stream.uniq_code,
                "streamName": stream.stream_name,
                "filePath": stream.file_path,
                "fps": stream.fps,
                "resolution": stream.resolution,
                "loopEnabled": stream.loop_enabled,
                "status": stream.status,
                "snapshotPath": stream.snapshot_path,
                "rtspUrl": get_rtsp_url(stream.uniq_code),  # ← derived from uniq_code
            }
            for stream in stream_list
        ]

        return (
            success_response(
                "List of streams retrieved successfully.",
                stream_data,
            ),
            200,
        )

    # async def get_stream(self, uniq_code):

    #     stream = await self.stream_repo.find_by_uniq_code(uniq_code)

    #     if not stream:
    #         return (
    #             error_response("Stream not found."),
    #             404,
    #         )

    #     return (
    #         success_response(
    #             "Stream fetched successfully.",
    #             stream.to_dict(),
    #         ),
    #         200,
    #     )

    # async def update_stream(self, data):

    #     stream = await self.stream_repo.find_by_uniq_code(data["uniqCode"])

    #     if not stream:
    #         return (
    #             error_response("Stream not found."),
    #             404,
    #         )

    #     updated = await self.stream_repo.update(stream, data)

    #     return (
    #         success_response(
    #             "Stream updated successfully.",
    #             updated.to_dict(),
    #         ),
    #         200,
    #     )

    # async def delete_stream(self, uniq_code):

    #     stream = await self.stream_repo.find_by_uniq_code(uniq_code)

    #     if not stream:
    #         return (
    #             error_response("Stream not found."),
    #             404,
    #         )

    #     await self.stream_repo.delete(stream)

    #     return (
    #         success_response("Stream deleted successfully."),
    #         200,
    #     )
