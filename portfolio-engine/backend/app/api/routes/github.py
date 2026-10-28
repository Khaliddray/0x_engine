from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.github import GitHubService

router = APIRouter(prefix="/api/github", tags=["github"])


@router.get("/repos")
def get_github_repositories(
    username: str = Query("Khaliddray", description="GitHub username to query"),
    force_refresh: bool = Query(False, description="Bypass cache and force refresh from GitHub"),
    db: Session = Depends(get_db),
):
    """
    Retrieve public GitHub repositories for the specified user.
    Uses in-memory caching with TTL and enriches with portfolio featured metadata.
    """
    service = GitHubService(username=username)
    return service.fetch_repositories(db=db, force_refresh=force_refresh)
