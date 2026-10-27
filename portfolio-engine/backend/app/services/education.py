from sqlalchemy.orm import Session

from app.models.education import Education
from app.repositories.education import EducationRepository
from app.repositories.portfolio import PortfolioRepository
from app.schemas.education import EducationCreate, EducationUpdate


class PortfolioNotFoundError(Exception):
    pass


class EducationNotFoundError(Exception):
    pass


class EducationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = EducationRepository(db)
        self.portfolio_repository = PortfolioRepository(db)

    def create(self, data: EducationCreate) -> Education:
        portfolio = self.portfolio_repository.get_by_id(data.portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {data.portfolio_id} not found."
            )

        education = Education(
            portfolio_id=data.portfolio_id,
            institution=data.institution,
            degree=data.degree,
            field_of_study=data.field_of_study,
            location=data.location,
            start_date=data.start_date,
            end_date=data.end_date,
            description=data.description,
            position=data.position,
            is_visible=data.is_visible,
        )

        return self.repository.create(education)

    def get_all(self) -> list[Education]:
        return self.repository.get_all()

    def get_by_id(self, education_id: int) -> Education:
        education = self.repository.get_by_id(education_id)

        if education is None:
            raise EducationNotFoundError(
                f"Education with ID {education_id} not found."
            )

        return education

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[Education]:
        portfolio = self.portfolio_repository.get_by_id(portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {portfolio_id} not found."
            )

        return self.repository.get_by_portfolio_id(portfolio_id)

    def update(
        self,
        education_id: int,
        data: EducationUpdate,
    ) -> Education:
        education = self.get_by_id(education_id)

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
            setattr(education, field, value)

        return self.repository.update(education)

    def delete(self, education_id: int) -> None:
        education = self.get_by_id(education_id)

        self.repository.delete(education)
