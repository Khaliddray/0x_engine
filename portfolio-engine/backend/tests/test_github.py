from unittest.mock import MagicMock, patch
import urllib.error

from app.services.github import GitHubService, _CACHE_STORE


def test_github_repos_endpoint(client):
    response = client.get("/api/github/repos")
    assert response.status_code == 200
    data = response.json()
    assert "repos" in data
    assert data["username"] == "Khaliddray"
    assert "profile_url" in data
    assert isinstance(data["repos"], list)

    if data["repos"]:
        first = data["repos"][0]
        assert "name" in first
        assert "html_url" in first
        assert "is_featured" in first
        assert "stars" in first
        assert "language" in first


def test_github_service_caching():
    _CACHE_STORE.clear()
    service = GitHubService("Khaliddray")

    # First fetch (fresh)
    res1 = service.fetch_repositories(force_refresh=True)
    if not res1.get("error"):
        assert res1["cached"] is False

        # Second fetch (cached)
        res2 = service.fetch_repositories(force_refresh=False)
        assert res2["cached"] is True
        assert res2["total"] == res1["total"]


def test_github_rate_limit_graceful_handling():
    _CACHE_STORE.clear()
    service = GitHubService("Khaliddray")

    # Mock urllib.request.urlopen to raise a 403 HTTPError (rate limit)
    with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError(
        url="https://api.github.com/users/Khaliddray/repos",
        code=403,
        msg="Rate Limit Exceeded",
        hdrs={},
        fp=None,
    )):
        result = service.fetch_repositories(force_refresh=True)
        assert result["total"] == 0
        assert result["error"] == "rate_limited"
        assert "rate limit exceeded" in result["message"].lower()
        assert result["profile_url"] == "https://github.com/Khaliddray"


def test_projects_page_renders_product_showcase(client):
    response = client.get("/projects", headers={"Accept": "text/html"})
    assert response.status_code == 200
    html = response.text
    assert "Featured Products" in html
    assert "02 //" in html
    assert "PRODUCT SHOWCASE" in html
    assert "Portfolio Engine" in html
    assert "Explore Product" in html
    assert "Product in Development" in html
    # Ensure GitHub repo metadata and raw repo scripts are not rendered in project listings
    assert "initial-repos-data" not in html


def test_projects_showcase_api_endpoint(client):
    response = client.get("/api/projects/showcase")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) >= 3
    names = [p["name"] for p in products]
    assert "Portfolio Engine" in names
    assert "Distributed Event Pipeline" in names
    assert "AuthGuard Zero-Trust Gateway" in names

