from datetime import date


def test_portfolio_crud_and_slug_conflict(client, auth_headers):
    # 1. Create portfolio
    create_res = client.post(
        "/api/portfolios",
        json={
            "name": "Original Portfolio",
            "slug": "original-portfolio",
            "description": "Initial description",
        },
        headers=auth_headers,
    )
    assert create_res.status_code == 201
    portfolio_id = create_res.json()["id"]

    # 2. Duplicate slug should return 409 Conflict
    conflict_res = client.post(
        "/api/portfolios",
        json={
            "name": "Duplicate Slug Portfolio",
            "slug": "original-portfolio",
        },
        headers=auth_headers,
    )
    assert conflict_res.status_code == 409
    assert "already exists" in conflict_res.json()["detail"]

    # 3. Get all and get by ID
    get_all_res = client.get("/api/portfolios")
    assert get_all_res.status_code == 200
    assert len(get_all_res.json()) >= 1

    get_one_res = client.get(f"/api/portfolios/{portfolio_id}")
    assert get_one_res.status_code == 200
    assert get_one_res.json()["name"] == "Original Portfolio"

    # 4. Patch update
    patch_res = client.patch(
        f"/api/portfolios/{portfolio_id}",
        json={"name": "Renamed Portfolio"},
        headers=auth_headers,
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["name"] == "Renamed Portfolio"

    # 5. Delete
    del_res = client.delete(
        f"/api/portfolios/{portfolio_id}",
        headers=auth_headers,
    )
    assert del_res.status_code == 204

    # 6. Verify 404 after deletion
    assert client.get(f"/api/portfolios/{portfolio_id}").status_code == 404


def test_portfolio_sections_crud(client, auth_headers):
    # Create parent portfolio
    p_res = client.post(
        "/api/portfolios",
        json={"name": "Section Portfolio", "slug": "section-port"},
        headers=auth_headers,
    )
    p_id = p_res.json()["id"]

    # 1. Create section
    s_res = client.post(
        "/api/sections",
        json={
            "portfolio_id": p_id,
            "title": "Bio",
            "slug": "bio-section",
            "type": "narrative",
            "content": "Full biography",
            "position": 1,
        },
        headers=auth_headers,
    )
    assert s_res.status_code == 201
    s_id = s_res.json()["id"]

    # 2. Duplicate section slug conflict
    conflict_res = client.post(
        "/api/sections",
        json={
            "portfolio_id": p_id,
            "title": "Another Bio",
            "slug": "bio-section",
            "type": "narrative",
        },
        headers=auth_headers,
    )
    assert conflict_res.status_code == 409

    # 3. Nonexistent portfolio should return 404
    nonexistent_res = client.post(
        "/api/sections",
        json={
            "portfolio_id": 9999,
            "title": "Ghost",
            "slug": "ghost-section",
            "type": "narrative",
        },
        headers=auth_headers,
    )
    assert nonexistent_res.status_code == 404

    # 4. List by portfolio
    list_res = client.get(f"/api/sections/portfolio/{p_id}")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # 5. Patch update
    patch_res = client.patch(
        f"/api/sections/{s_id}",
        json={"title": "Updated Bio"},
        headers=auth_headers,
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["title"] == "Updated Bio"

    # 6. Delete section
    del_res = client.delete(f"/api/sections/{s_id}", headers=auth_headers)
    assert del_res.status_code == 204
    assert client.get(f"/api/sections/{s_id}").status_code == 404


def test_skills_crud(client, auth_headers):
    # Create parent portfolio
    p_res = client.post(
        "/api/portfolios",
        json={"name": "Skill Portfolio", "slug": "skill-port"},
        headers=auth_headers,
    )
    p_id = p_res.json()["id"]

    # 1. Create skill
    sk_res = client.post(
        "/api/skills",
        json={
            "portfolio_id": p_id,
            "name": "PostgreSQL",
            "slug": "postgresql",
            "category": "Databases",
            "proficiency": "Advanced",
            "position": 1,
        },
        headers=auth_headers,
    )
    assert sk_res.status_code == 201
    sk_id = sk_res.json()["id"]

    # 2. Duplicate slug conflict
    conflict_res = client.post(
        "/api/skills",
        json={
            "portfolio_id": p_id,
            "name": "Postgres Duplicate",
            "slug": "postgresql",
        },
        headers=auth_headers,
    )
    assert conflict_res.status_code == 409

    # 3. Patch skill
    patch_res = client.patch(
        f"/api/skills/{sk_id}",
        json={"proficiency": "Expert"},
        headers=auth_headers,
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["proficiency"] == "Expert"

    # 4. Delete skill
    assert client.delete(f"/api/skills/{sk_id}", headers=auth_headers).status_code == 204
    assert client.get(f"/api/skills/{sk_id}").status_code == 404


def test_experience_and_education_crud(client, auth_headers):
    # Create parent portfolio
    p_res = client.post(
        "/api/portfolios",
        json={"name": "History Portfolio", "slug": "history-port"},
        headers=auth_headers,
    )
    p_id = p_res.json()["id"]

    # Experience CRUD
    exp_res = client.post(
        "/api/experiences",
        json={
            "portfolio_id": p_id,
            "company": "Tech Corp",
            "role": "Lead Architect",
            "start_date": "2023-01-01",
            "description": "Systems architecture",
        },
        headers=auth_headers,
    )
    assert exp_res.status_code == 201
    exp_id = exp_res.json()["id"]

    assert client.get(f"/api/experiences/portfolio/{p_id}").status_code == 200
    assert client.patch(f"/api/experiences/{exp_id}", json={"role": "Principal Architect"}, headers=auth_headers).status_code == 200
    assert client.delete(f"/api/experiences/{exp_id}", headers=auth_headers).status_code == 204

    # Education CRUD
    edu_res = client.post(
        "/api/education",
        json={
            "portfolio_id": p_id,
            "institution": "State University",
            "degree": "B.Sc.",
            "field_of_study": "Software Engineering",
            "start_date": "2018-09-01",
        },
        headers=auth_headers,
    )
    assert edu_res.status_code == 201
    edu_id = edu_res.json()["id"]

    assert client.get(f"/api/education/portfolio/{p_id}").status_code == 200
    assert client.patch(f"/api/education/{edu_id}", json={"degree": "M.Sc."}, headers=auth_headers).status_code == 200
    assert client.delete(f"/api/education/{edu_id}", headers=auth_headers).status_code == 204


def test_certifications_and_social_links_crud(client, auth_headers):
    p_res = client.post(
        "/api/portfolios",
        json={"name": "Credentials Portfolio", "slug": "credentials-port"},
        headers=auth_headers,
    )
    p_id = p_res.json()["id"]

    # Certification CRUD
    cert_res = client.post(
        "/api/certifications",
        json={
            "portfolio_id": p_id,
            "name": "AWS Certified Architect",
            "issuer": "Amazon Web Services",
            "issue_date": "2024-05-01",
        },
        headers=auth_headers,
    )
    assert cert_res.status_code == 201
    cert_id = cert_res.json()["id"]

    assert client.get(f"/api/certifications/portfolio/{p_id}").status_code == 200
    assert client.patch(f"/api/certifications/{cert_id}", json={"name": "AWS Solutions Architect Pro"}, headers=auth_headers).status_code == 200
    assert client.delete(f"/api/certifications/{cert_id}", headers=auth_headers).status_code == 204

    # Social Link CRUD
    soc_res = client.post(
        "/api/social-links",
        json={
            "portfolio_id": p_id,
            "platform": "GitHub",
            "url": "https://github.com/developer",
        },
        headers=auth_headers,
    )
    assert soc_res.status_code == 201
    soc_id = soc_res.json()["id"]

    assert client.get(f"/api/social-links/portfolio/{p_id}").status_code == 200
    assert client.patch(f"/api/social-links/{soc_id}", json={"label": "Developer GitHub"}, headers=auth_headers).status_code == 200
    assert client.delete(f"/api/social-links/{soc_id}", headers=auth_headers).status_code == 204


def test_resumes_primary_toggle_logic(client, auth_headers):
    p_res = client.post(
        "/api/portfolios",
        json={"name": "Resume Portfolio", "slug": "resume-port"},
        headers=auth_headers,
    )
    p_id = p_res.json()["id"]

    # 1. Create primary resume
    r1_res = client.post(
        "/api/resumes",
        json={
            "portfolio_id": p_id,
            "title": "Resume 2024",
            "file_url": "https://example.com/r1.pdf",
            "version": "1.0",
            "is_primary": True,
        },
        headers=auth_headers,
    )
    assert r1_res.status_code == 201
    r1_id = r1_res.json()["id"]
    assert r1_res.json()["is_primary"] is True

    # 2. Create second resume marked as primary -> r1 should become non-primary
    r2_res = client.post(
        "/api/resumes",
        json={
            "portfolio_id": p_id,
            "title": "Resume 2025",
            "file_url": "https://example.com/r2.pdf",
            "version": "2.0",
            "is_primary": True,
        },
        headers=auth_headers,
    )
    assert r2_res.status_code == 201
    r2_id = r2_res.json()["id"]
    assert r2_res.json()["is_primary"] is True

    # Verify r1 is no longer primary
    r1_updated = client.get(f"/api/resumes/{r1_id}").json()
    assert r1_updated["is_primary"] is False


def test_project_technologies_and_media_crud(client, auth_headers):
    p_res = client.post(
        "/api/portfolios",
        json={"name": "Project Children Portfolio", "slug": "project-children-port"},
        headers=auth_headers,
    )
    p_id = p_res.json()["id"]

    prj_res = client.post(
        "/api/projects",
        json={
            "portfolio_id": p_id,
            "title": "Core API",
            "slug": "core-api",
            "description": "API Gateway",
        },
        headers=auth_headers,
    )
    assert prj_res.status_code == 201
    prj_id = prj_res.json()["id"]

    # Project Technology CRUD
    tech_res = client.post(
        "/api/project-technologies",
        json={
            "project_id": prj_id,
            "name": "Docker",
            "slug": "docker",
            "position": 1,
        },
        headers=auth_headers,
    )
    assert tech_res.status_code == 201
    tech_id = tech_res.json()["id"]

    assert client.get(f"/api/project-technologies/project/{prj_id}").status_code == 200
    assert client.patch(f"/api/project-technologies/{tech_id}", json={"name": "Docker Compose"}, headers=auth_headers).status_code == 200
    assert client.delete(f"/api/project-technologies/{tech_id}", headers=auth_headers).status_code == 204

    # Project Media CRUD
    media_res = client.post(
        "/api/project-media",
        json={
            "project_id": prj_id,
            "url": "https://example.com/screenshot.png",
            "alt_text": "System Architecture",
            "caption": "Architecture diagram",
            "position": 1,
        },
        headers=auth_headers,
    )
    assert media_res.status_code == 201
    media_id = media_res.json()["id"]

    assert client.get(f"/api/project-media/project/{prj_id}").status_code == 200
    assert client.patch(f"/api/project-media/{media_id}", json={"alt_text": "Updated Diagram"}, headers=auth_headers).status_code == 200
    assert client.delete(f"/api/project-media/{media_id}", headers=auth_headers).status_code == 204
