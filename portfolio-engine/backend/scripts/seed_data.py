"""Database seed script for Portfolio Engine.

Populates accurate portfolio data for Yahaya Khalid, verified projects (Portfolio Engine),
genuine technical stack, product building journey, and an administrator account for local development.
"""

from datetime import date
from pathlib import Path
import sys

# Ensure backend root is on sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models import (
    Certification,
    Education,
    Experience,
    Portfolio,
    PortfolioSection,
    Project,
    ProjectMedia,
    ProjectTechnology,
    Resume,
    Skill,
    SocialLink,
    User,
)


import os
import sys

def seed_database(if_empty: bool = False) -> None:
    # Ensure all tables exist
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        existing_portfolio = db.query(Portfolio).first()
        if if_empty and existing_portfolio:
            print("• Database already initialized with portfolio data. Skipping automatic seed.")
            return

        admin_email = os.getenv("ADMIN_EMAIL", "khalidzak21@gmail.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "1234567Khalid")
        admin_name = os.getenv("ADMIN_NAME", "Yahaya Khalid")

        # 1. Seed or retrieve superuser
        user = db.query(User).filter_by(is_superuser=True).first()
        if not user:
            user = User(
                email=admin_email,
                hashed_password=hash_password(admin_password),
                full_name=admin_name,
                is_active=True,
                is_superuser=True,
            )
            db.add(user)
            db.flush()
            print(f"✓ Created admin user: {admin_email}")
        else:
            print(f"• Admin user already exists: {user.email}")

        # 2. Seed or update Portfolio
        portfolio = db.query(Portfolio).filter_by(slug="khalid").first()
        if not portfolio:
            portfolio = Portfolio(
                name="Yahaya Khalid",
                slug="khalid",
                description=(
                    "I turn ideas into working software, with a focus on backend engineering, "
                    "thoughtful design, and solving problems that matter."
                ),
            )
            db.add(portfolio)
            db.flush()
            print("✓ Created portfolio: Yahaya Khalid (slug: khalid)")
        else:
            portfolio.description = (
                "I turn ideas into working software, with a focus on backend engineering, "
                "thoughtful design, and solving problems that matter."
            )
            db.flush()
            print("✓ Updated portfolio: Yahaya Khalid (slug: khalid)")

        portfolio_id = portfolio.id

        # Clean existing dependent data for a clean re-seed
        existing_projects = db.query(Project).filter_by(portfolio_id=portfolio_id).all()
        for p in existing_projects:
            db.query(ProjectTechnology).filter_by(project_id=p.id).delete()
            db.query(ProjectMedia).filter_by(project_id=p.id).delete()
        db.query(Project).filter_by(portfolio_id=portfolio_id).delete()
        db.query(PortfolioSection).filter_by(portfolio_id=portfolio_id).delete()
        db.query(Skill).filter_by(portfolio_id=portfolio_id).delete()
        db.query(Experience).filter_by(portfolio_id=portfolio_id).delete()
        db.query(Education).filter_by(portfolio_id=portfolio_id).delete()
        db.query(Certification).filter_by(portfolio_id=portfolio_id).delete()
        db.query(SocialLink).filter_by(portfolio_id=portfolio_id).delete()
        db.query(Resume).filter_by(portfolio_id=portfolio_id).delete()
        db.flush()

        # 3. Seed Portfolio Sections
        sections = [
            PortfolioSection(
                portfolio_id=portfolio_id,
                title="About Me",
                slug="about-me",
                type="narrative",
                content=(
                    "I'm a software developer and product builder focused on building useful software, "
                    "designing maintainable backend systems, and turning ideas into working products. "
                    "My core focus centers on backend engineering, API development, database design, "
                    "product development, and maintainable software architecture that can grow with its purpose."
                ),
                position=1,
                is_visible=True,
            ),
            PortfolioSection(
                portfolio_id=portfolio_id,
                title="Engineering Philosophy",
                slug="engineering-philosophy",
                type="philosophy",
                content=(
                    "Build what solves the problem. Keep the architecture understandable. "
                    "Design data models carefully, separate responsibilities, and build products "
                    "that can evolve as requirements change."
                ),
                position=2,
                is_visible=True,
            ),
        ]
        db.add_all(sections)
        db.flush()
        print(f"✓ Created {len(sections)} portfolio sections")

        # 4. Seed Verified Project: Portfolio Engine
        prj_engine = Project(
            portfolio_id=portfolio_id,
            title="Portfolio Engine",
            slug="portfolio-engine",
            description=(
                "A dynamic, content-driven portfolio management API that allows portfolio information and "
                "projects to be managed through structured backend endpoints. It is designed to support future "
                "growth without rebuilding the entire portfolio whenever the owner's career develops."
            ),
            github_url="https://github.com/Khaliddray/0x_engine",
            live_url="/docs",
            is_featured=True,
        )
        db.add(prj_engine)
        db.flush()

        # Add Verified Technologies to Portfolio Engine
        techs = [
            ProjectTechnology(project_id=prj_engine.id, name="Python", slug="python", position=1),
            ProjectTechnology(project_id=prj_engine.id, name="FastAPI", slug="fastapi", position=2),
            ProjectTechnology(project_id=prj_engine.id, name="PostgreSQL", slug="postgresql", position=3),
            ProjectTechnology(project_id=prj_engine.id, name="SQLAlchemy", slug="sqlalchemy", position=4),
            ProjectTechnology(project_id=prj_engine.id, name="Alembic", slug="alembic", position=5),
            ProjectTechnology(project_id=prj_engine.id, name="Pydantic", slug="pydantic", position=6),
            ProjectTechnology(project_id=prj_engine.id, name="Pytest", slug="pytest", position=7),
            ProjectTechnology(project_id=prj_engine.id, name="Docker", slug="docker", position=8),
        ]
        db.add_all(techs)

        # Add Media
        media = [
            ProjectMedia(
                project_id=prj_engine.id,
                url="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1000&auto=format&fit=crop&q=80",
                alt_text="Portfolio Engine Architecture",
                caption="FastAPI REST API Layer, SQLAlchemy Repositories, and Alembic Migrations",
                position=1,
            ),
        ]
        db.add_all(media)
        db.flush()
        print("✓ Created Portfolio Engine project with technologies and architecture media")

        # 5. Seed Genuine Technical Stack (no unverified proficiency levels)
        skills = [
            Skill(portfolio_id=portfolio_id, name="Python", slug="python", category="Languages", proficiency=None, position=1),
            Skill(portfolio_id=portfolio_id, name="FastAPI", slug="fastapi", category="Frameworks", proficiency=None, position=2),
            Skill(portfolio_id=portfolio_id, name="PostgreSQL", slug="postgresql", category="Databases", proficiency=None, position=3),
            Skill(portfolio_id=portfolio_id, name="SQLAlchemy", slug="sqlalchemy", category="Data Access & ORM", proficiency=None, position=4),
            Skill(portfolio_id=portfolio_id, name="Alembic", slug="alembic", category="Database Migrations", proficiency=None, position=5),
            Skill(portfolio_id=portfolio_id, name="Pydantic", slug="pydantic", category="Validation & Schemas", proficiency=None, position=6),
            Skill(portfolio_id=portfolio_id, name="REST APIs", slug="rest-api", category="Architecture", proficiency=None, position=7),
            Skill(portfolio_id=portfolio_id, name="Git & GitHub", slug="git-github", category="Version Control", proficiency=None, position=8),
            Skill(portfolio_id=portfolio_id, name="Docker", slug="docker", category="Containerization", proficiency=None, position=9),
            Skill(portfolio_id=portfolio_id, name="Pytest", slug="pytest", category="Testing & Automation", proficiency=None, position=10),
        ]
        db.add_all(skills)
        db.flush()
        print(f"✓ Created {len(skills)} verified skills")

        # 6. Seed Journey (Focus on Product Building & Backend Engineering)
        experiences = [
            Experience(
                portfolio_id=portfolio_id,
                company="Product Building & Backend Systems",
                role="Product Builder & Backend Engineer",
                employment_type="Independent Engineering",
                location="Abuja, Nigeria",
                start_date=date(2023, 1, 1),
                end_date=None,
                description=(
                    "Focused on building purposeful digital products, designing maintainable backend systems, "
                    "and turning ideas into working software. Designed and implemented Portfolio Engine from the "
                    "ground up as a production-grade, content-driven portfolio management API with layered architecture "
                    "(Routes → Services → Repositories → Models), partial PATCH updates, Argon2 authentication, "
                    "Alembic database migrations, and 100% passing automated Pytest test suites."
                ),
                position=1,
                is_visible=True,
            ),
        ]
        db.add_all(experiences)
        db.flush()
        print("✓ Created Journey entry")

        # 7. Seed Verified Social & Contact Links
        links = [
            SocialLink(portfolio_id=portfolio_id, platform="GitHub", url="https://github.com/Khaliddray", label="github.com/Khaliddray", position=1, is_visible=True),
            SocialLink(portfolio_id=portfolio_id, platform="LinkedIn", url="https://www.linkedin.com/in/yahaya-khalid-198593418", label="linkedin.com/in/yahaya-khalid-198593418", position=2, is_visible=True),
            SocialLink(portfolio_id=portfolio_id, platform="X", url="https://www.x.com/Zzaq_0x", label="x.com/Zzaq_0x", position=3, is_visible=True),
            SocialLink(portfolio_id=portfolio_id, platform="Email", url="mailto:khalidzak21@gmail.com", label="khalidzak21@gmail.com", position=4, is_visible=True),
        ]
        db.add_all(links)
        db.flush()
        print(f"✓ Created {len(links)} verified social and contact links")

        db.commit()
        print("\n Seeding completed successfully with accurate, verified developer data!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    if_empty_flag = "--if-empty" in sys.argv
    seed_database(if_empty=if_empty_flag)
