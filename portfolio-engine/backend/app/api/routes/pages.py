from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.api.deps import get_db
from app.core.products import PRODUCTS
from app.core.templates import templates
from app.services.public_portfolio import (
    PublicPortfolioNotFoundError,
    PublicPortfolioService,
)

router = APIRouter(tags=["pages"])

TICKER_TECHS = [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "SQLAlchemy",
    "Alembic",
    "Pydantic",
    "REST APIs",
    "Pytest",
    "Docker",
    "Git & GitHub",
]

VERIFIED_STACK = [
    {
        "category": "Languages",
        "name": "Python",
        "description": "Primary backend language. Implemented across REST endpoints, automated test suites, and data models.",
        "verified": True,
    },
    {
        "category": "Frameworks",
        "name": "FastAPI",
        "description": "High-performance asynchronous Python API framework with dependency injection and Pydantic contracts.",
        "verified": True,
    },
    {
        "category": "Databases",
        "name": "PostgreSQL",
        "description": "Primary relational storage for portfolios, projects, and users with relational constraints.",
        "verified": True,
    },
    {
        "category": "Data Access & ORM",
        "name": "SQLAlchemy",
        "description": "SQLAlchemy 2.0 declarative models, repository design patterns, and transactional sessions.",
        "verified": True,
    },
    {
        "category": "Database Migrations",
        "name": "Alembic",
        "description": "Version-controlled database schema migrations managing evolution and table constraints.",
        "verified": True,
    },
    {
        "category": "Validation & Schemas",
        "name": "Pydantic",
        "description": "Pydantic v2 schemas enforcing strict request payload validation and response contracts.",
        "verified": True,
    },
    {
        "category": "Architecture",
        "name": "REST APIs",
        "description": "Layered architecture cleanly separating Routes, Services, Repositories, and Database Models.",
        "verified": True,
    },
    {
        "category": "Version Control",
        "name": "Git & GitHub",
        "description": "Disciplined version control, incremental commits, atomic changes, and repository management.",
        "verified": True,
    },
    {
        "category": "Containerization",
        "name": "Docker",
        "description": "Multi-container orchestration with Dockerfile and Docker Compose for API and PostgreSQL.",
        "verified": True,
    },
    {
        "category": "Testing & Automation",
        "name": "Pytest",
        "description": "Automated test suite with isolated in-memory SQLite fixtures verifying routes, repositories, and auth.",
        "verified": True,
    },
]


def _get_portfolio_safely(db: Session, slug: str = "khalid"):
    service = PublicPortfolioService(db)
    try:
        return service.get_by_slug(slug)
    except PublicPortfolioNotFoundError:
        return None


@router.get("/")
def home_page(
    request: Request,
    db: Session = Depends(get_db),
):
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        portfolio = _get_portfolio_safely(db, "khalid")
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "portfolio": portfolio,
                "ticker_techs": TICKER_TECHS,
                "current_route": "home",
            },
        )

    return {
        "name": "Portfolio Engine API",
        "version": "0.1.0",
        "status": "running",
    }


@router.get("/about")
def about_page(
    request: Request,
    db: Session = Depends(get_db),
):
    portfolio = _get_portfolio_safely(db, "khalid")
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "request": request,
            "portfolio": portfolio,
            "current_route": "about",
        },
    )


@router.get("/projects")
def projects_page(
    request: Request,
    db: Session = Depends(get_db),
):
    portfolio = _get_portfolio_safely(db, "khalid")
    return templates.TemplateResponse(
        request=request,
        name="projects.html",
        context={
            "request": request,
            "portfolio": portfolio,
            "products": PRODUCTS,
            "current_route": "projects",
        },
    )


@router.get("/stack")
def stack_page(
    request: Request,
    db: Session = Depends(get_db),
):
    portfolio = _get_portfolio_safely(db, "khalid")
    return templates.TemplateResponse(
        request=request,
        name="stack.html",
        context={
            "request": request,
            "portfolio": portfolio,
            "verified_stack": VERIFIED_STACK,
            "current_route": "stack",
        },
    )


@router.get("/journey")
def journey_page(
    request: Request,
    db: Session = Depends(get_db),
):
    portfolio = _get_portfolio_safely(db, "khalid")
    return templates.TemplateResponse(
        request=request,
        name="journey.html",
        context={
            "request": request,
            "portfolio": portfolio,
            "current_route": "journey",
        },
    )


@router.get("/contact")
def contact_page(
    request: Request,
    db: Session = Depends(get_db),
):
    portfolio = _get_portfolio_safely(db, "khalid")
    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={
            "request": request,
            "portfolio": portfolio,
            "current_route": "contact",
        },
    )


@router.get("/portfolio/{slug}")
@router.get("/portfolio")
def view_portfolio_slug(
    request: Request,
    slug: str = "khalid",
    db: Session = Depends(get_db),
):
    portfolio = _get_portfolio_safely(db, slug)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "portfolio": portfolio,
            "ticker_techs": TICKER_TECHS,
            "current_route": "home",
        },
    )


@router.get("/admin")
def admin_page(
    request: Request,
    db: Session = Depends(get_db),
):
    portfolio = _get_portfolio_safely(db, "khalid")
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "request": request,
            "portfolio": portfolio,
            "current_route": "admin",
        },
    )

