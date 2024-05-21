from datetime import datetime

from sqlalchemy import Column, ForeignKey, func, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class VacancySkills(Base):
    __tablename__ = "vacancies_skills"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    vacancy_id: "Vacancy" = Column(ForeignKey("vacancies.id", ondelete="CASCADE"))
    skill_name: str = Column(String)

    def __str__(self):
        return self.skill_name


class Vacancy(Base):
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
