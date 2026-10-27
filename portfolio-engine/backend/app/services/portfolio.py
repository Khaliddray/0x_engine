from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.repositories.portfolio import PortfolioRepository
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate


class PortfolioSlugExistsError(Exception):
    """Raised when a portfolio slug already exists."""


class PortfolioService:
    def __init__(self, db: Session):
        self.repository = PortfolioRepository(db)

    def create(self, data: PortfolioCreate) -> Portfolio:
        existing_portfolio = self.repository.get_by_slug(data.slug)

        if existing_portfolio is not None:
            raise PortfolioSlugExistsError("Portfolio slug already exists")

        portfolio = Portfolio(
            name=data.name,
            slug=data.slug,
            description=data.description,
        )

        return self.repository.create(portfolio)

    def get_all(self) -> list[Portfolio]:
        return self.repository.get_all()

    def get_by_id(self, portfolio_id: int) -> Portfolio | None:
        return self.repository.get_by_id(portfolio_id)

    def update(
        self,
        portfolio_id: int,
        data: PortfolioUpdate,
    ) -> Portfolio | None:
        portfolio = self.repository.get_by_id(portfolio_id)

        if portfolio is None:
            return None

        update_data = data.model_dump(exclude_unset=True)

        if "slug" in update_data:
            existing_portfolio = self.repository.get_by_slug(
                update_data["slug"]
            )

            if (
                existing_portfolio is not None
                and existing_portfolio.id != portfolio_id
            ):
                raise PortfolioSlugExistsError("Portfolio slug already exists")

        for field, value in update_data.items():
            setattr(portfolio, field, value)

        return self.repository.update(portfolio)

    def delete(self, portfolio_id: int) -> bool:
        portfolio = self.repository.get_by_id(portfolio_id)

        if portfolio is None:
            return False

        self.repository.delete(portfolio)
        return True
