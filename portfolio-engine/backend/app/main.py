from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes.health import router as health_router
from app.api.routes.portfolios import router as portfolio_router
from app.api.routes.projects import router as project_router
from app.api.routes.portfolio_sections import router as portfolio_section_router
from app.api.routes.skills import router as skill_router
from app.api.routes.experiences import router as experience_router
from app.api.routes.education import router as education_router
from app.api.routes.certifications import router as certification_router
from app.api.routes.social_links import router as social_link_router
from app.api.routes.resumes import router as resume_router
from app.api.routes.project_technologies import router as project_technology_router
from app.api.routes.project_media import router as project_media_router
from app.api.routes.public_portfolios import router as public_portfolio_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as user_router
from app.api.routes.admin import router as admin_router
from app.api.routes.contact import router as contact_router


app = FastAPI(
    title="Portfolio Engine API",
    description="Backend API for a dynamic, content-driven personal portfolio.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(portfolio_router)
app.include_router(project_router)
app.include_router(portfolio_section_router)
app.include_router(skill_router)
app.include_router(experience_router)
app.include_router(education_router)
app.include_router(certification_router)
app.include_router(social_link_router)
app.include_router(resume_router)
app.include_router(project_technology_router)
app.include_router(project_media_router)
app.include_router(public_portfolio_router)
app.include_router(contact_router)

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
FRONTEND_DIST_INDEX = FRONTEND_DIR / "dist" / "index.html"
FRONTEND_SRC_INDEX = FRONTEND_DIR / "index.html"


def get_frontend_index() -> Path | None:
    if FRONTEND_DIST_INDEX.is_file():
        return FRONTEND_DIST_INDEX
    if FRONTEND_SRC_INDEX.is_file():
        return FRONTEND_SRC_INDEX
    return None


if FRONTEND_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def root(request: Request):
    accept_header = request.headers.get("accept", "")
    frontend_file = get_frontend_index()
    if "text/html" in accept_header and frontend_file:
        return FileResponse(frontend_file)

    return {
        "name": "Portfolio Engine API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/portfolio/{slug}")
@app.get("/portfolio")
def view_portfolio(slug: str | None = None):
    frontend_file = get_frontend_index()
    if frontend_file:
        return FileResponse(frontend_file)
    return {"message": "Frontend not found"}

