"""
This module defines the models for users and their related entities.

Classes:
    User: Represents a user of the application.
    UserVacancy: Represents the relationship between a user and a vacancy.
"""
from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime,
    BigInteger,
)
from sqlalchemy.orm import relationship

from . import JobSeeker
from .base import Base
from .vacancy import Vacancy



class User(Base):
    """
    Represents a user of the application.

    Attributes:
        id (int): The primary key identifier for the user.
        created_at (datetime): The date and time when the user was created.
        job_seeker_id (int): The foreign key referencing the associated jobseeker profile.
        job_seeker (JobSeeker): The jobseeker profile associated with the user.
    """
    __tablename__ = "user"

    id: int = Column(BigInteger, primary_key=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    job_seeker_id = Column(
        Integer, ForeignKey("job_seeker.id", ondelete="SET NULL"), nullable=True
    )
    job_seeker: JobSeeker = relationship("JobSeeker", uselist=False)


class UserVacancy(Base):
    """
   Represents the relationship between a user and a vacancy.

   Attributes:
       id (int): The primary key identifier for the user-vacancy relationship.
       user_id (int): The foreign key referencing the associated user.
       vacancy_id (int): The foreign key referencing the associated vacancy.
   """

    __tablename__ = "user_vacancies"

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id: int = Column(ForeignKey(User.id, ondelete="CASCADE"))
    vacancy_id: int = Column(ForeignKey(Vacancy.id, ondelete="CASCADE"))
