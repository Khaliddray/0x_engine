from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.repositories.portfolio import PortfolioRepository
from app.repositories.skill import SkillRepository
from app.schemas.skill import SkillCreate, SkillUpdate


class PortfolioNotFoundError(Exception):
    pass


class SkillNotFoundError(Exception):
    pass


class SkillSlugExistsError(Exception):
    pass


class SkillService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = SkillRepository(db)
        self.portfolio_repository = PortfolioRepository(db)

    def create(
        self,
        data: SkillCreate,
    ) -> Skill:
        portfolio = self.portfolio_repository.get_by_id(
            data.portfolio_id,
        )

        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio with ID {data.portfolio_id} not found."
            )

        existing_skill = self.repository.get_by_slug(
            data.slug
        )

        if existing_skill is not None:
            raise SkillSlugExistsError(
                f"Skill with slug '{data.slug}' already exists."
            )

        skill = Skill(
            portfolio_id=data.portfolio_id,
            name=data.name,
            slug=data.slug,
            category=data.category,
            proficiency=data.proficiency,
            position=data.position,
            is_visible=data.is_visible,
        )

        return self.repository.create(skill)

    def get_all(self) -> list[Skill]:
        return self.repository.get_all()

    def get_by_id(
        self,
        skill_id: int,
    ) -> Skill:
        skill = self.repository.get_by_id(skill_id)

        if skill is None:
            raise SkillNotFoundError(
                f"Skill with ID {skill_id} not found."
            )

        return skill

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[Skill]:
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
        skill_id: int,
        data: SkillUpdate,
    ) -> Skill:
        skill = self.get_by_id(skill_id)

        updates = data.model_dump(
            exclude_unset=True
        )

        if "portfolio_id" in updates:
            portfolio = self.portfolio_repository.get_by_id(
                updates["portfolio_id"],
            )

            if portfolio is None:
                raise PortfolioNotFoundError(
                    f"Portfolio with ID {updates['portfolio_id']} not found."
                )

        if "slug" in updates and updates["slug"] != skill.slug:
            existing_skill = self.repository.get_by_slug(
                updates["slug"]
            )

            if existing_skill is not None:
                raise SkillSlugExistsError(
                    f"Skill with slug '{updates['slug']}' already exists."
                )

        for field, value in updates.items():
            setattr(skill, field, value)

        return self.repository.update(skill)

    def delete(
        self,
        skill_id: int,
    ) -> None:
        skill = self.get_by_id(skill_id)
        self.repository.delete(skill)
