from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
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
from app.api.routes.github import router as github_router
from app.api.routes.pages import router as pages_router
from app.core.config import settings
from app.core.templates import templates
from starlette.responses import FileResponse, JSONResponse


app = FastAPI(
    title=settings.app_name,
    description="Backend API for a dynamic, content-driven personal portfolio.",
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


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
app.include_router(github_router)

STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "static"

if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.api_route("/favicon.ico", methods=["GET", "HEAD"], include_in_schema=False)
async def favicon():
    favicon_path = STATIC_DIR / "favicon.ico"
    if favicon_path.is_file():
        return FileResponse(favicon_path, media_type="image/x-icon")
    return JSONResponse(status_code=404, content={"detail": "Favicon not found"})


# Mount dedicated HTML page route handlers
app.include_router(pages_router)



@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header and not request.url.path.startswith("/api/"):
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={"request": request, "current_route": "404"},
            status_code=404,
        )
    detail = getattr(exc, "detail", "Not Found")
    return JSONResponse(status_code=404, content={"detail": detail})

