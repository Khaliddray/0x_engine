from sqlalchemy.orm import Session

from app.models.portfolio_section import PortfolioSection
from app.repositories.portfolio import PortfolioRepository
from app.repositories.portfolio_section import PortfolioSectionRepository
from app.schemas.portfolio_section import (
    PortfolioSectionCreate,
    PortfolioSectionUpdate,
)


class PortfolioNotFoundError(Exception):
    pass


class PortfolioSectionNotFoundError(Exception):
    pass


class PortfolioSectionSlugExistsError(Exception):
    pass


class PortfolioSectionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PortfolioSectionRepository(db)
        self.portfolio_repository = PortfolioRepository(db)

    def create(
        self,
        data: PortfolioSectionCreate,
    ) -> PortfolioSection:
        portfolio = self.portfolio_repository.get_by_id(data.portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {data.portfolio_id} not found."
            )

        existing_section = self.repository.get_by_slug(data.slug)

        if existing_section is not None:
            raise PortfolioSectionSlugExistsError(
                f"Section with slug '{data.slug}' already exists."
            )

        section = PortfolioSection(
            portfolio_id=data.portfolio_id,
            title=data.title,
            slug=data.slug,
            type=data.type,
            content=data.content,
            position=data.position,
            is_visible=data.is_visible,
        )

        return self.repository.create(section)

    def get_all(self) -> list[PortfolioSection]:
        return self.repository.get_all()

    def get_by_id(self, section_id: int) -> PortfolioSection:
        section = self.repository.get_by_id(section_id)

        if section is None:
            raise PortfolioSectionNotFoundError(
                f"Portfolio section with ID {section_id} not found."
            )

        return section

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[PortfolioSection]:
        portfolio = self.portfolio_repository.get_by_id(portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {portfolio_id} not found."
            )

        return self.repository.get_by_portfolio_id(portfolio_id)

    def update(
        self,
        section_id: int,
        data: PortfolioSectionUpdate,
    ) -> PortfolioSection:
        section = self.get_by_id(section_id)

        updates = data.model_dump(exclude_unset=True)

        if "portfolio_id" in updates:
            portfolio = self.portfolio_repository.get_by_id(
                updates["portfolio_id"],
            )

            if portfolio is None:
                raise PortfolioNotFoundError(
                    f"Portfolio with ID {updates['portfolio_id']} not found."
                )

        if "slug" in updates and updates["slug"] != section.slug:
            existing_section = self.repository.get_by_slug(
                updates["slug"]
            )

            if existing_section is not None:
                raise PortfolioSectionSlugExistsError(
                    f"Section with slug '{updates['slug']}' already exists."
                )

        for field, value in updates.items():
            setattr(section, field, value)

        return self.repository.update(section)

    def delete(self, section_id: int) -> None:
        section = self.get_by_id(section_id)
        self.repository.delete(section)
