from enum import Enum
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum as SqlEnum,
)
from app.database.base import Base


class Stream(Base):
    __tablename__ = "streams"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Unique stream identifier
    uniq_code = Column(String(20), unique=True, nullable=False, index=True)

    # User defined name
    stream_name = Column(String(100), nullable=False)

    # Absolute/local storage path
    file_path = Column(String(500))
    
    snapshot_path = Column(String(500))

    # Stream configuration
    fps = Column(Integer, default=15)

    resolution = Column(String(20), default="1280x720")

    loop_enabled = Column(Boolean, default=True)

    status = Column(Boolean, default=True)
