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
    __tablename__ = "user"

    id: int = Column(BigInteger, primary_key=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    job_seeker_id = Column(
        Integer, ForeignKey("job_seeker.id", ondelete="SET NULL"), nullable=True
    )
    job_seeker: JobSeeker = relationship("JobSeeker", uselist=False)


class UserVacancy(Base):
    __tablename__ = "user_vacancies"

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id = Column(ForeignKey(User.id, ondelete="CASCADE"))
    vacancy_id = Column(ForeignKey(Vacancy.id, ondelete="CASCADE"))
