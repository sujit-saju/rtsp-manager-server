from app.models.stream_entity import Stream
from app.repositories.stream_repository import StreamRepository
from app.utils.response import success_response, error_response
from app.services.unique_code_service import UniqueCodeService


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
        )

        stream = await self.stream_repo.create(new_stream)

        return (
            success_response(
                "Stream created successfully.",
                {
                    "streamName": stream.stream_name,
                    "fps": stream.fps,
                    "uniqCode": stream.uniq_code,
                    "resolution": stream.resolution,
                    "status": stream.status,
                    "loopEnabled": stream.loop_enabled,
                },
            ),
            201,
        )

    # async def get_all_streams(self):

    #     streams = await self.stream_repo.find_all()

    #     return (
    #         success_response(
    #             "Streams fetched successfully.",
    #             [s.to_dict() for s in streams],
    #         ),
    #         200,
    #     )

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
