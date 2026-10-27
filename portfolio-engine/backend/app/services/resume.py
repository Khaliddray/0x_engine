from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.repositories.portfolio import PortfolioRepository
from app.repositories.resume import ResumeRepository
from app.schemas.resume import ResumeCreate, ResumeUpdate


class PortfolioNotFoundError(Exception):
    pass


class ResumeNotFoundError(Exception):
    pass


class ResumeService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ResumeRepository(db)
        self.portfolio_repository = PortfolioRepository(db)

    def _set_primary_resume(
        self,
        portfolio_id: int,
        exclude_resume_id: int | None = None,
    ) -> None:
        statement = (
            update(Resume)
            .where(
                Resume.portfolio_id == portfolio_id,
                Resume.is_primary.is_(True),
            )
            .values(is_primary=False)
        )

        if exclude_resume_id is not None:
            statement = statement.where(
                Resume.id != exclude_resume_id
            )

        self.db.execute(statement)

    def create(self, data: ResumeCreate) -> Resume:
        portfolio = self.portfolio_repository.get_by_id(
            data.portfolio_id,
        )

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {data.portfolio_id} not found."
            )

        if data.is_primary:
            self._set_primary_resume(
                portfolio_id=data.portfolio_id,
            )

        resume = Resume(
            portfolio_id=data.portfolio_id,
            title=data.title,
            file_url=data.file_url,
            version=data.version,
            description=data.description,
            is_primary=data.is_primary,
            is_visible=data.is_visible,
        )

        return self.repository.create(resume)

    def get_all(self) -> list[Resume]:
        return self.repository.get_all()

    def get_by_id(self, resume_id: int) -> Resume:
        resume = self.repository.get_by_id(resume_id)

        if resume is None:
            raise ResumeNotFoundError(
                f"Resume with ID {resume_id} not found."
            )

        return resume

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[Resume]:
        portfolio = self.portfolio_repository.get_by_id(
            portfolio_id,
        )

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {portfolio_id} not found."
            )

        return self.repository.get_by_portfolio_id(
            portfolio_id
        )

    def update(
        self,
        resume_id: int,
        data: ResumeUpdate,
    ) -> Resume:
        resume = self.get_by_id(resume_id)

        updates = data.model_dump(
            exclude_unset=True
        )

        target_portfolio_id = updates.get(
            "portfolio_id",
            resume.portfolio_id,
        )

        if "portfolio_id" in updates:
            portfolio = self.portfolio_repository.get_by_id(
                updates["portfolio_id"],
            )

            if portfolio is None:
                raise PortfolioNotFoundError(
                    f"Portfolio with ID {updates['portfolio_id']} not found."
                )

        if updates.get("is_primary") is True:
            self._set_primary_resume(
                portfolio_id=target_portfolio_id,
                exclude_resume_id=resume.id,
            )

        for field, value in updates.items():
            setattr(resume, field, value)

        return self.repository.update(resume)

    def delete(self, resume_id: int) -> None:
        resume = self.get_by_id(resume_id)

        self.repository.delete(resume)
