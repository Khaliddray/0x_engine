from sqlalchemy.orm import Session

from app.models.experience import Experience
from app.repositories.experience import ExperienceRepository
from app.repositories.portfolio import PortfolioRepository
from app.schemas.experience import ExperienceCreate, ExperienceUpdate


class PortfolioNotFoundError(Exception):
    pass


class ExperienceNotFoundError(Exception):
    pass


class ExperienceService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ExperienceRepository(db)
        self.portfolio_repository = PortfolioRepository(db)

    def create(self, data: ExperienceCreate) -> Experience:
        portfolio = self.portfolio_repository.get_by_id(data.portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {data.portfolio_id} not found."
            )

        experience = Experience(
            portfolio_id=data.portfolio_id,
            company=data.company,
            role=data.role,
            employment_type=data.employment_type,
            location=data.location,
            start_date=data.start_date,
            end_date=data.end_date,
            description=data.description,
            position=data.position,
            is_visible=data.is_visible,
        )

        return self.repository.create(experience)

    def get_all(self) -> list[Experience]:
        return self.repository.get_all()

    def get_by_id(self, experience_id: int) -> Experience:
        experience = self.repository.get_by_id(experience_id)

        if experience is None:
            raise ExperienceNotFoundError(
                f"Experience with ID {experience_id} not found."
            )

        return experience

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[Experience]:
        portfolio = self.portfolio_repository.get_by_id(portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {portfolio_id} not found."
            )

        return self.repository.get_by_portfolio_id(portfolio_id)

    def update(
        self,
        experience_id: int,
        data: ExperienceUpdate,
    ) -> Experience:
        experience = self.get_by_id(experience_id)

        updates = data.model_dump(exclude_unset=True)

        if "portfolio_id" in updates:
            portfolio = self.portfolio_repository.get_by_id(
                updates["portfolio_id"]
            )

            if portfolio is None:
                raise PortfolioNotFoundError(
                    f"Portfolio with ID {updates['portfolio_id']} not found."
                )

        for field, value in updates.items():
            setattr(experience, field, value)

        return self.repository.update(experience)

    def delete(self, experience_id: int) -> None:
        experience = self.get_by_id(experience_id)
        self.repository.delete(experience)
