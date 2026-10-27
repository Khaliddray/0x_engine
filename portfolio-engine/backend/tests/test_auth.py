def test_register_user_success(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "ValidPassword123!",
            "full_name": "New User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email_conflict(client, test_user):
    response = client.post(
        "/api/auth/register",
        json={
            "email": test_user.email,
            "password": "AnotherPassword123!",
            "full_name": "Duplicate User",
        },
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_login_success(client, test_user):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "developer@example.com",
            "password": "DevPassword123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client, test_user):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "developer@example.com",
            "password": "IncorrectPassword!",
        },
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_nonexistent_email(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "ghost@example.com",
            "password": "SomePassword123!",
        },
    )
    assert response.status_code == 401


def test_get_current_user_profile(client, auth_headers, test_user):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email


def test_get_current_user_unauthorized(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_users_list_requires_superuser(client, auth_headers, superuser_headers):
    # Standard user receives 403 Forbidden
    std_res = client.get("/api/users", headers=auth_headers)
    assert std_res.status_code == 403

    # Superuser receives 200 OK
    su_res = client.get("/api/users", headers=superuser_headers)
    assert su_res.status_code == 200
    assert len(su_res.json()) >= 1


def test_oauth2_token_login_success(client, test_user):
    response = client.post(
        "/api/auth/token",
        data={
            "username": "developer@example.com",
            "password": "DevPassword123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_oauth2_token_login_invalid(client, test_user):
    response = client.post(
        "/api/auth/token",
        data={
            "username": "developer@example.com",
            "password": "WrongPassword!",
        },
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_cors_headers_present(client):
    response = client.options(
        "/api/auth/me",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert "GET" in response.headers.get("access-control-allow-methods", "")
