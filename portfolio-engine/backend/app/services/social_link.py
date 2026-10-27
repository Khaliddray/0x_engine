from sqlalchemy.orm import Session

from app.models.social_link import SocialLink
from app.repositories.portfolio import PortfolioRepository
from app.repositories.social_link import SocialLinkRepository
from app.schemas.social_link import SocialLinkCreate, SocialLinkUpdate


class PortfolioNotFoundError(Exception):
    pass


class SocialLinkNotFoundError(Exception):
    pass


class SocialLinkService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = SocialLinkRepository(db)
        self.portfolio_repository = PortfolioRepository(db)

    def create(self, data: SocialLinkCreate) -> SocialLink:
        portfolio = self.portfolio_repository.get_by_id(data.portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {data.portfolio_id} not found."
            )

        social_link = SocialLink(
            portfolio_id=data.portfolio_id,
            platform=data.platform,
            url=data.url,
            label=data.label,
            position=data.position,
            is_visible=data.is_visible,
        )

        return self.repository.create(social_link)

    def get_all(self) -> list[SocialLink]:
        return self.repository.get_all()

    def get_by_id(self, social_link_id: int) -> SocialLink:
        social_link = self.repository.get_by_id(social_link_id)

        if social_link is None:
            raise SocialLinkNotFoundError(
                f"Social link with ID {social_link_id} not found."
            )

        return social_link

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[SocialLink]:
        portfolio = self.portfolio_repository.get_by_id(portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {portfolio_id} not found."
            )

        return self.repository.get_by_portfolio_id(portfolio_id)

    def update(
        self,
        social_link_id: int,
        data: SocialLinkUpdate,
    ) -> SocialLink:
        social_link = self.get_by_id(social_link_id)

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
            setattr(social_link, field, value)

        return self.repository.update(social_link)

    def delete(self, social_link_id: int) -> None:
        social_link = self.get_by_id(social_link_id)

        self.repository.delete(social_link)
