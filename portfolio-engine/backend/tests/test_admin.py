def test_admin_overview_unauthorized_without_token(client):
    response = client.get("/api/admin/overview")
    assert response.status_code == 401


def test_admin_overview_authorized_empty(client, auth_headers):
    response = client.get("/api/admin/overview", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_portfolios"] == 0
    assert data["total_projects"] == 0
    assert data["total_featured_projects"] == 0
    assert data["total_sections"] == 0
    assert data["total_skills"] == 0
    assert data["total_users"] == 1


def test_admin_overview_reflects_created_entities(client, auth_headers):
    # 1. Create a portfolio
    p_res = client.post(
        "/api/portfolios",
        json={"name": "Engineering Portfolio", "slug": "eng-portfolio"},
        headers=auth_headers,
    )
    assert p_res.status_code == 201
    portfolio_id = p_res.json()["id"]

    # 2. Create featured and normal projects
    client.post(
        "/api/projects",
        json={
            "portfolio_id": portfolio_id,
            "title": "Engine",
            "slug": "engine-prj",
            "is_featured": True,
        },
        headers=auth_headers,
    )
    client.post(
        "/api/projects",
        json={
            "portfolio_id": portfolio_id,
            "title": "Side Project",
            "slug": "side-prj",
            "is_featured": False,
        },
        headers=auth_headers,
    )

    # 3. Create a skill
    client.post(
        "/api/skills",
        json={
            "portfolio_id": portfolio_id,
            "name": "Python",
            "slug": "python",
        },
        headers=auth_headers,
    )

    # 4. Query admin overview
    res = client.get("/api/admin/overview", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total_portfolios"] == 1
    assert data["total_projects"] == 2
    assert data["total_featured_projects"] == 1
    assert data["total_skills"] == 1


def test_mutation_endpoints_require_authentication(client):
    endpoints = [
        ("POST", "/api/portfolios", {"name": "P", "slug": "p"}),
        ("PATCH", "/api/portfolios/1", {"name": "P2"}),
        ("DELETE", "/api/portfolios/1", None),
        ("POST", "/api/projects", {"portfolio_id": 1, "title": "Prj", "slug": "prj"}),
        ("PATCH", "/api/projects/1", {"title": "Updated"}),
        ("DELETE", "/api/projects/1", None),
        ("POST", "/api/sections", {"portfolio_id": 1, "title": "S", "slug": "s"}),
        ("POST", "/api/skills", {"portfolio_id": 1, "name": "Sk", "slug": "sk"}),
        ("POST", "/api/experiences", {"portfolio_id": 1, "company": "C", "role": "R", "start_date": "2024-01-01"}),
        ("POST", "/api/education", {"portfolio_id": 1, "institution": "U", "degree": "B", "field_of_study": "F", "start_date": "2020-01-01"}),
        ("POST", "/api/certifications", {"portfolio_id": 1, "name": "C", "issuing_organization": "O", "issue_date": "2024-01-01"}),
        ("POST", "/api/social-links", {"portfolio_id": 1, "platform": "P", "url": "https://p.com"}),
        ("POST", "/api/resumes", {"portfolio_id": 1, "file_name": "r.pdf", "file_url": "https://r.pdf"}),
        ("POST", "/api/project-technologies", {"project_id": 1, "name": "T", "slug": "t"}),
        ("POST", "/api/project-media", {"project_id": 1, "media_type": "image", "url": "https://img.png"}),
    ]

    for method, path, payload in endpoints:
        if method == "POST":
            res = client.post(path, json=payload)
        elif method == "PATCH":
            res = client.patch(path, json=payload)
        elif method == "DELETE":
            res = client.delete(path)
        assert res.status_code == 401, f"{method} {path} should require authentication, got {res.status_code}"


def test_admin_page_renders_html(client):
    response = client.get("/admin", headers={"Accept": "text/html"})
    assert response.status_code == 200
    html = response.text
    assert "Control Center" in html
    assert "0X // ADMINISTRATION" in html
    assert "Authenticate" in html
    assert "Database Projects Management" in html
    assert "Skills &amp; Technical Stack Management" in html or "Skills & Technical Stack Management" in html
    assert "Narrative Sections Management" in html


