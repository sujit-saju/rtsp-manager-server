# ============================================
# File     : stream_repository.py
# Author   : Sujit
# Created  : 2026-06-10
# Desc     : Repository for Stream data access,
#            extending base CRUD operations
# ============================================

from app.repositories.base import BaseRepository
from app.models.stream_entity import Stream
from sqlalchemy import func, select
from sqlalchemy.orm import Session


class StreamRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Stream)

    async def find_by_stream_name(self, stream_name: str):
        result = await self.db.execute(
            select(Stream).where(Stream.stream_name == stream_name)
        )
        return result.scalars().first()
    
    async def create(self, stream_obj: Stream):
        self.db.add(stream_obj)

        await self.db.commit()
        await self.db.refresh(stream_obj)

        return stream_obj
