import json
import logging
import time
import urllib.error
import urllib.request
from typing import Any, Optional
from sqlalchemy.orm import Session

from app.repositories.portfolio import PortfolioRepository
from app.repositories.project import ProjectRepository

logger = logging.getLogger(__name__)

# In-memory repository cache with 10-minute TTL
_CACHE_STORE: dict[str, dict[str, Any]] = {}
CACHE_TTL_SECONDS = 600  # 10 minutes


class GitHubService:
    def __init__(self, username: str = "Khaliddray"):
        self.username = username
        self.api_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=100"

    def fetch_repositories(
        self,
        db: Optional[Session] = None,
        force_refresh: bool = False,
    ) -> dict[str, Any]:
        """
        Fetch public repositories for the configured user from the GitHub REST API.
        Implements in-memory TTL caching, graceful rate-limit handling, and
        associates manually featured projects from the database.
        """
        now = time.time()
        cached_entry = _CACHE_STORE.get(self.username)

        if not force_refresh and cached_entry:
            if now - cached_entry["timestamp"] < CACHE_TTL_SECONDS:
                return {
                    "repos": cached_entry["repos"],
                    "cached": True,
                    "stale": False,
                    "total": len(cached_entry["repos"]),
                    "username": self.username,
                    "profile_url": f"https://github.com/{self.username}",
                }

        req = urllib.request.Request(
            self.api_url,
            headers={
                "User-Agent": "PortfolioEngine/1.0",
                "Accept": "application/vnd.github.v3+json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                raw_data = json.loads(response.read().decode("utf-8"))

                # Map manual featured projects from DB if db session is available
                featured_map: dict[str, Any] = {}
                if db:
                    portfolio_repo = PortfolioRepository(db)
                    portfolio = portfolio_repo.get_by_slug("khalid")
                    if portfolio:
                        project_repo = ProjectRepository(db)
                        db_projects = project_repo.get_by_portfolio_id(portfolio.id)
                        for p in db_projects:
                            if p.github_url:
                                normalized_url = p.github_url.rstrip("/").lower()
                                featured_map[normalized_url] = p
                            # Also match by repository name / slug
                            featured_map[p.slug.lower()] = p

                processed_repos = []
                for item in raw_data:
                    repo_html_url = item.get("html_url", "")
                    normalized_repo_url = repo_html_url.rstrip("/").lower()
                    repo_name = item.get("name", "")

                    # Check if repo matches an existing database project marked as featured
                    db_match = featured_map.get(normalized_repo_url) or featured_map.get(repo_name.lower())
                    is_featured = bool(db_match.is_featured) if db_match else False

                    # Check homepage for valid demo URL (only http:// or https://)
                    homepage = (item.get("homepage") or "").strip()
                    if not (homepage.startswith("http://") or homepage.startswith("https://")):
                        homepage = None

                    processed_repos.append({
                        "id": item.get("id"),
                        "name": repo_name,
                        "full_name": item.get("full_name"),
                        "description": item.get("description"),
                        "language": item.get("language"),
                        "stars": item.get("stargazers_count", 0),
                        "forks": item.get("forks_count", 0),
                        "is_fork": item.get("fork", False),
                        "topics": item.get("topics") or [],
                        "html_url": repo_html_url,
                        "homepage": homepage,
                        "updated_at": item.get("updated_at"),
                        "created_at": item.get("created_at"),
                        "is_featured": is_featured,
                        "db_project_id": db_match.id if db_match else None,
                        "db_project_slug": db_match.slug if db_match else None,
                    })

                _CACHE_STORE[self.username] = {
                    "repos": processed_repos,
                    "timestamp": now,
                }

                return {
                    "repos": processed_repos,
                    "cached": False,
                    "stale": False,
                    "total": len(processed_repos),
                    "username": self.username,
                    "profile_url": f"https://github.com/{self.username}",
                }

        except urllib.error.HTTPError as e:
            logger.warning("GitHub API HTTP error %d: %s", e.code, e.reason)
            is_rate_limit = (e.code == 403)
            # If we have stale cache, serve it with a warning
            if cached_entry:
                return {
                    "repos": cached_entry["repos"],
                    "cached": True,
                    "stale": True,
                    "warning": "GitHub API rate limit or error; serving cached data.",
                    "total": len(cached_entry["repos"]),
                    "username": self.username,
                    "profile_url": f"https://github.com/{self.username}",
                }
            return {
                "repos": [],
                "cached": False,
                "stale": False,
                "error": "rate_limited" if is_rate_limit else f"http_error_{e.code}",
                "message": (
                    "GitHub API rate limit exceeded. Please view my repositories directly on GitHub."
                    if is_rate_limit
                    else f"GitHub API error ({e.code}). Please view my repositories directly on GitHub."
                ),
                "total": 0,
                "username": self.username,
                "profile_url": f"https://github.com/{self.username}",
            }
        except Exception as e:
            logger.error("GitHub API unexpected error: %s", e)
            if cached_entry:
                return {
                    "repos": cached_entry["repos"],
                    "cached": True,
                    "stale": True,
                    "warning": "Network error; serving cached data.",
                    "total": len(cached_entry["repos"]),
                    "username": self.username,
                    "profile_url": f"https://github.com/{self.username}",
                }
            return {
                "repos": [],
                "cached": False,
                "stale": False,
                "error": "network_error",
                "message": "Could not connect to GitHub API. Please check your network or visit my GitHub profile directly.",
                "total": 0,
                "username": self.username,
                "profile_url": f"https://github.com/{self.username}",
            }
