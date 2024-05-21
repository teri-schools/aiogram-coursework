"""
This module defines the models for jobseekers and their related entities.

Classes:
    JobSeekerSkills: Represents a skill associated with a jobseeker.
    JobSeeker: Represents a jobseeker with their personal information and skills.
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class JobSeekerSkills(Base):
    """
    Represents a skill associated with a jobseeker.

    Attributes:
       id (int): The primary key identifier for the skill.
       job_seeker_id (int): The foreign key referencing the associated jobseeker.
       skill_name (str): The name of the skill.
    """
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
    """
    Represents a jobseeker with their personal information and skills.

    Attributes:
        id (int): The primary key identifier for the jobseeker.
        first_name (str): The first name of the jobseeker.
        last_name (str): The last name of the jobseeker.
        middle_name (str): The middle name of the jobseeker.
        email (str): The email address of the jobseeker.
        phone_number (str): The phone number of the jobseeker.
        experience (int): The work experience of the jobseeker in years.
        skills (list[JobSeekerSkills]): The list of skills associated with the jobseeker.
    """
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
