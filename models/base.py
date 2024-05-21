from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    metadata = MetaData()
    __allow_unmapped__ = True
    # type_annotation_map = {
    #     str: String,
    #     int: Integer,
    #     bool: Boolean,
    #     float: Float,
    #     datetime: DateTime,
    #     date: Date,
    # }
