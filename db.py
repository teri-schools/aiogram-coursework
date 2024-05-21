from sqlalchemy import URL, select, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL as CONFIG_DATABASE_URL
from models import User, JobSeeker, JobSeekerSkills, UserVacancy, Vacancy, VacancySkills


def get_async_engine(url: str | URL = CONFIG_DATABASE_URL) -> AsyncEngine:
    async_engine = create_async_engine(url)
    return async_engine


def get_async_sessionmake(async_engine: AsyncEngine) -> sessionmaker[AsyncSession]:
    # Async session maker
    async_session = sessionmaker(async_engine, class_=AsyncSession)
    return async_session  # type: ignore


class Repo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def add_user(self, user_id: int):
        user = User(id=user_id)
        self.session.add(user)
        await self.session.commit()

    async def paginate_jobseeker(self, index: int) -> JobSeeker:
        stmp = (
            select(JobSeeker)
            .options(selectinload(JobSeeker.skills))
            .order_by(desc(JobSeeker.id))
            .offset(index)
        )
        return await self.session.scalar(stmp)

    async def get_jobseeker(self, jobseeker_id: int) -> JobSeeker:
        stmp = (
            select(JobSeeker)
            .options(selectinload(JobSeeker.skills))
            .where(JobSeeker.id == jobseeker_id)
        )
        return await self.session.scalar(stmp)

    async def delete_jobseeker(self, jobseeker_id: int):
        stmp = delete(JobSeeker).where(JobSeeker.id == jobseeker_id)
        await self.session.execute(stmp)
        await self.session.commit()

    async def add_jobseeker(self, user_id: int, data: dict):
        user = await self.session.get(User, user_id)
        # add jobseeker
        job_seeker = JobSeeker(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            middle_name=data.get("middle_name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            experience=data.get("experience"),
        )
        self.session.add(job_seeker)
        # update id
        await self.session.flush([job_seeker])
        # add skills
        for skill in data.get("skills", []):
            self.session.add(
                JobSeekerSkills(job_seeker_id=job_seeker.id, skill_name=skill)
            )
        # add jobseeker to user
        user.job_seeker_id = job_seeker.id
        # save
        await self.session.commit()

    async def get_vacancy(self, vacancy_id: int) -> Vacancy:
        stmp = (
            select(Vacancy)
            .options(selectinload(Vacancy.skills))
            .where(Vacancy.id == vacancy_id)
        )
        return await self.session.scalar(stmp)

    async def get_vacancy_user_id(self, vacancy_id: int):
        stmp = select(UserVacancy.user_id).where(UserVacancy.vacancy_id == vacancy_id)
        return await self.session.scalar(stmp)

    async def paginate_user_vacancies(self, user_id: int, index: int) -> Vacancy:
        stmp = (
            select(Vacancy)
            .options(selectinload(Vacancy.skills))
            .where(User.id == user_id)
            .order_by(desc(Vacancy.id))
            .offset(index)
        )
        return await self.session.scalar(stmp)

    async def paginate_vacencies(self, index: int) -> Vacancy:
        stmp = (
            select(Vacancy)
            .options(selectinload(Vacancy.skills))
            .order_by(desc(Vacancy.id))
            .offset(index)
        )
        return await self.session.scalar(stmp)

    async def paginate_vacancies(self, user_id: int, index: int) -> Vacancy:
        stmp = (
            select(Vacancy)
            .options(selectinload(Vacancy.skills))
            .join(User.posted_vacancies)
            .where(User.id == user_id)
            .order_by(desc(Vacancy.id))
            .offset(index)
        )
        return await self.session.scalar(stmp)

    async def add_vacancy(self, user_id: int, data: dict):
        vacancy = Vacancy(
            title=data.get("title"),
            description=data.get("description"),
            company_name=data.get("company_name"),
            location=data.get("location"),
            salary=data.get("salary"),
        )
        self.session.add(vacancy)
        await self.session.flush([vacancy])
        for skill in data.get("skills", []):
            self.session.add(VacancySkills(vacancy_id=vacancy.id, skill_name=skill))
        self.session.add(UserVacancy(user_id=user_id, vacancy_id=vacancy.id))
        await self.session.commit()

    async def delete_vacancy(self, vacancy_id: int):
        stmp = delete(Vacancy).where(Vacancy.id == vacancy_id)
        await self.session.execute(stmp)
        await self.session.commit()
