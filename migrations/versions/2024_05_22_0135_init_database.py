"""init database

Revision ID: 76c30aaeddc7
Revises: 
Create Date: 2024-05-22 01:35:17.340232

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "76c30aaeddc7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "job_seeker",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("middle_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=True),
        sa.Column("experience", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vacancies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("company_name", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("salary", sa.Integer(), nullable=True),
        sa.Column(
            "posted_date",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "job_seeker_skills",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("job_seeker_id", sa.Integer(), nullable=False),
        sa.Column("skill_name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["job_seeker_id"], ["job_seeker.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("job_seeker_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["job_seeker_id"], ["job_seeker.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vacancies_skills",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("vacancy_id", sa.Integer(), nullable=True),
        sa.Column("skill_name", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["vacancy_id"], ["vacancies.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_vacancies",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("vacancy_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["vacancy_id"], ["vacancies.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_vacancies")
    op.drop_table("vacancies_skills")
    op.drop_table("user")
    op.drop_table("job_seeker_skills")
    op.drop_table("vacancies")
    op.drop_table("job_seeker")
    # ### end Alembic commands ###
