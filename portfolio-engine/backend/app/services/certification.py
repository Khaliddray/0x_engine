from sqlalchemy.orm import Session

from app.models.certification import Certification
from app.repositories.certification import CertificationRepository
from app.repositories.portfolio import PortfolioRepository
from app.schemas.certification import CertificationCreate, CertificationUpdate


class PortfolioNotFoundError(Exception):
    pass


class CertificationNotFoundError(Exception):
    pass


class CertificationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CertificationRepository(db)
        self.portfolio_repository = PortfolioRepository(db)

    def create(self, data: CertificationCreate) -> Certification:
        portfolio = self.portfolio_repository.get_by_id(data.portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {data.portfolio_id} not found."
            )

        certification = Certification(
            portfolio_id=data.portfolio_id,
            name=data.name,
            issuer=data.issuer,
            credential_id=data.credential_id,
            credential_url=data.credential_url,
            issue_date=data.issue_date,
            expiration_date=data.expiration_date,
            description=data.description,
            position=data.position,
            is_visible=data.is_visible,
        )

        return self.repository.create(certification)

    def get_all(self) -> list[Certification]:
        return self.repository.get_all()

    def get_by_id(self, certification_id: int) -> Certification:
        certification = self.repository.get_by_id(certification_id)

        if certification is None:
            raise CertificationNotFoundError(
                f"Certification with ID {certification_id} not found."
            )

        return certification

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[Certification]:
        portfolio = self.portfolio_repository.get_by_id(portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {portfolio_id} not found."
            )

        return self.repository.get_by_portfolio_id(portfolio_id)

    def update(
        self,
        certification_id: int,
        data: CertificationUpdate,
    ) -> Certification:
        certification = self.get_by_id(certification_id)

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
            setattr(certification, field, value)

        return self.repository.update(certification)

    def delete(self, certification_id: int) -> None:
        certification = self.get_by_id(certification_id)

        self.repository.delete(certification)
