from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class JobSeekerSkills(Base):
    __tablename__ = "job_seeker_skills"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    job_seeker_id: int = Column(
        Integer, ForeignKey("job_seeker.id", ondelete="CASCADE"), nullable=False
    )
    skill_name: str = Column(String, nullable=False)

    # level: int = Column(Integer, nullable=False)

    def __str__(self) -> str:
        return self.skill_name


# class JobSeekerEducation(Base):
#     __tablename__ = "job_seeker_educations"
#
#     id: int = Column(Integer, primary_key=True, autoincrement=True)
#
#     job_seeker_id: int = Column(Integer, ForeignKey("job_seeker.id"), nullable=False)
#     degree: str = Column(String, nullable=False)
#     specialty: str = Column(String, nullable=False)
#     institution: str = Column(String, nullable=False)
#     start: date = Column(Date, nullable=False)
#     end: date = Column(Date, nullable=False)
#
#     def __str__(self):
#         return f"{self.institution}"


class JobSeeker(Base):
    __tablename__ = "job_seeker"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    middle_name: str = Column(String, nullable=False)

    email: str = Column(String, nullable=False)
    phone_number: str = Column(String, nullable=True)

    experience: int = Column(Integer, nullable=True)

    skills: list[JobSeekerSkills] = relationship(JobSeekerSkills, uselist=True)

    # educations: list[JobSeekerEducation] = relationship(
    #     JobSeekerEducation, uselist=True
    # )
    # resumes: str = Column(String, nullable=True)

    @property
    def short_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __repr__(self):
        return f"<JobSeeker(id={self.id}, name={self.first_name} {self.last_name}, email={self.email})>"
