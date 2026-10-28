# Portfolio Engine

Portfolio Engine is a content-driven personal portfolio system built with FastAPI and PostgreSQL. It is designed to cleanly separate portfolio content and data management from presentation concerns, allowing frontend interfaces to evolve independently.

---

## Architecture

The backend follows a strict layered architecture:

```text
HTTP Clients / Frontend
       ↓
    Routes          (HTTP handling, parameter validation, status codes)
       ↓
   Services         (Business logic, validation rules, cross-resource orchestration)
       ↓
 Repositories       (Database queries, persistence operations)
       ↓
    Models          (SQLAlchemy ORM models & relationships)
       ↓
  PostgreSQL        (Relational storage)
```

- **Pydantic Schemas:** Enforce input validation and API contracts.
- **Route Protection:** All write operations (`POST`, `PATCH`, `DELETE`) require JWT authentication.
- **Public API:** Clean aggregated read endpoint (`/api/public/portfolios/{slug}`) optimized for frontend rendering.

---

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **ORM & DB:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/), [PostgreSQL](https://www.postgresql.org/), [psycopg 3](https://www.psycopg.org/)
- **Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
- **Validation:** [Pydantic v2](https://docs.pydantic.dev/) & [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **Security & Auth:** [Argon2](https://pypi.org/project/argon2-cffi/) password hashing, [PyJWT](https://pyjwt.readthedocs.io/) access tokens
- **Testing:** [Pytest](https://docs.pytest.org/) with isolated in-memory SQLite fixtures

---

## Repository Structure

```text
portfolio-engine/
├── AGENTS.md               # Architecture, domain, and agent development guidelines
├── README.md               # Project documentation and quickstart
├── docker-compose.yml      # Service orchestration
└── backend/
    ├── alembic.ini         # Alembic configuration
    ├── pytest.ini          # Pytest configuration
    ├── requirements.txt    # Python dependencies
    ├── alembic/            # Database migration versions
    ├── tests/              # Automated test suite
    └── app/
        ├── main.py         # FastAPI application entry point & router mounting
        ├── api/            # API routes and dependency injection (deps.py)
        ├── core/           # Configuration & cryptographic security helpers
        ├── db/             # Database session and base model definitions
        ├── models/         # SQLAlchemy database models
        ├── repositories/   # Persistence and data access layer
        ├── schemas/        # Pydantic request and response schemas
        └── services/       # Domain business logic and validation
```

---

## API Capabilities

### 1. Public Endpoints
- `GET /` — API service information and status.
- `GET /health` — Health check endpoint.
- `GET /api/public/portfolios/{slug}` — Complete aggregated portfolio data payload for frontend rendering.

### 2. Authentication & User Management
- `POST /api/auth/register` — Register a new account.
- `POST /api/auth/login` — Authenticate and receive a Bearer JWT access token.
- `GET /api/auth/me` — Retrieve current authenticated user profile.
- `GET /api/users` — List system users (Superuser only).

### 3. Administration
- `GET /api/admin/overview` — Aggregated counts and system metrics across portfolios, projects, and users.

### 4. Content Management (Authenticated)
Full CRUD endpoints with partial `PATCH` updates and slug conflict validation:
- `/api/portfolios`
- `/api/projects` (supports `is_featured` project flags)
- `/api/sections`
- `/api/skills`
- `/api/experiences`
- `/api/education`
- `/api/certifications`
- `/api/social-links`
- `/api/resumes`
- `/api/project-technologies`
- `/api/project-media`

---

## Getting Started

### 1. Prerequisites
- Python 3.12+
- PostgreSQL (or local SQLite for lightweight testing)

### 2. Environment Configuration
Copy `.env.example` to create your local `.env` file:

```bash
cp .env.example backend/.env
```

Ensure the database connection string uses the `postgresql+psycopg://` dialect for psycopg 3:

```env
DATABASE_URL=postgresql+psycopg://portfolio_user:portfolio_password@localhost:5432/portfolio_db
SECRET_KEY=replace-with-a-secure-random-secret-key-at-least-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Database Migrations
Run all Alembic migrations to initialize or update the database schema:
```bash
cd backend
alembic upgrade head
```

### 5. Running the API Server
Start the development server with live reload:
```bash
cd backend
uvicorn app.main:app --reload
```
Interactive API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- Admin Control Center: `http://localhost:8000/admin`

### 6. Running with Docker Compose (Recommended for Local Dev)
You can start the PostgreSQL database and FastAPI backend with a single command:

```bash
docker compose up --build
```

This will:
- Spin up PostgreSQL 16 on port 5432 with health check verification.
- Build the FastAPI container.
- Automatically execute `alembic upgrade head` to run all migrations.
- Automatically execute `python3 scripts/seed_data.py --if-empty` to populate initial portfolio data if empty.
- Serve the API and frontend on `http://localhost:8000`.

---

## Production Deployment

### 1. Render Blueprint (1-Click Deployment)
A complete `render.yaml` blueprint is included in the root directory:
1. Push your repository to GitHub.
2. In the Render Dashboard, click **New +** → **Blueprint**.
3. Select your repository.
4. Render will automatically provision a managed PostgreSQL database, link `DATABASE_URL`, build the Docker container using `backend/Dockerfile`, run migrations via `backend/scripts/entrypoint.sh`, and launch the web service with HTTPS.

### 2. Standard Container Platforms (Railway, Fly.io, Cloud Run, VPS)
The container uses `backend/scripts/entrypoint.sh` as its entrypoint, which:
1. Automatically runs `alembic upgrade head` to bring the database schema to the latest version.
2. Conditionally runs `python3 scripts/seed_data.py --if-empty` to initialize portfolio records and superuser credentials if the database is newly initialized.
3. Automatically binds to the cloud provider's injected `$PORT` environment variable (falling back to port 8000).

A `Procfile` is also provided in the repository root for process manager workflows:
```text
web: cd backend && alembic upgrade head && python3 scripts/seed_data.py --if-empty && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

---

## Running Automated Tests

The test suite runs against an isolated SQLite in-memory database and tests authentication, admin metrics, public aggregation, multi-page frontend routing, and repository operations:

```bash
pytest -c backend/pytest.ini backend/tests
```

