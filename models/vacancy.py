"""
This module defines the models for job vacancies and their related entities.

Classes:
    VacancySkills: Represents a skill required for a job vacancy.
    Vacancy: Represents a job vacancy with its details and required skills.
"""
from datetime import datetime

from sqlalchemy import Column, ForeignKey, func, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class VacancySkills(Base):
    """
    Represents a skill required for a job vacancy.

    Attributes:
        id (int): The primary key identifier for the skill.
        vacancy_id (Vacancy): The foreign key referencing the associated job vacancy.
        skill_name (str): The name of the skill.
    """
    __tablename__ = "vacancies_skills"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    vacancy_id: "Vacancy" = Column(ForeignKey("vacancies.id", ondelete="CASCADE"))
    skill_name: str = Column(String)

    def __str__(self):
        return self.skill_name


class Vacancy(Base):
    """
    Represents a job vacancy with its details and required skills.

    Attributes:
        id (int): The primary key identifier for the job vacancy.
        title (str): The title of the job vacancy.
        description (str): The description of the job vacancy.
        company_name (str): The name of the company offering the job vacancy.
        location (str): The location of the job vacancy.
        salary (int): The salary for the job vacancy.
        posted_date (datetime): The date when the job vacancy was posted.
        skills (list[VacancySkills]): The list of skills required for the job vacancy.
    """
    __tablename__ = "vacancies"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    title: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False)

    company_name: str = Column(String, nullable=False)
    location: str = Column(String, nullable=True)

    salary: int = Column(Integer, nullable=True)

    posted_date: datetime = Column(DateTime, server_default=func.now())

    skills = relationship(VacancySkills)

    def __str__(self):
        return (
            f"#id{self.id}\n"
            f"{self.title}\n"
            f"Заробітня плата: {self.salary}\n"
            f"Дата публікації: {self.posted_date}\n"
            f"Компанія: {self.company_name}\n"
            f"Розташування: {self.location}\n"
            f"Необхідні навички: {', '.join(map(str, self.skills))}\n\n"
            f"{self.description}"
        )
