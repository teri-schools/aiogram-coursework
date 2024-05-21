"""
This module defines the base class for SQLAlchemy models.

Classes:
    Base: A declarative base class for SQLAlchemy models.
"""
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    A declarative base class for SQLAlchemy models.

    This class inherits from the DeclarativeBase class provided by SQLAlchemy.
    It sets up the metadata for the models and allows for unmapped classes.
    """
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
