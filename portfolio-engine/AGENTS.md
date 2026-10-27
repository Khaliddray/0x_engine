# Portfolio Engine — Agent Instructions

## Project Purpose

Portfolio Engine is a long-term, content-driven personal portfolio system designed to present Yahaya Khalid's work professionally and remain easy to evolve as his career develops.

The system should make it possible to:

- Change the portfolio design without rewriting the backend.
- Add, remove, or replace projects as stronger work is completed.
- Add future portfolio sections without restructuring the entire application.
- Keep portfolio content separate from presentation concerns.

The project should demonstrate practical software engineering ability, not just serve as a static portfolio website.

---

## Current Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- pydantic-settings
- Uvicorn

### Frontend

- React-based frontend
- Frontend implementation is not yet the primary development focus.

---

## Backend Architecture

The backend follows a layered architecture:

    Routes
       ↓
    Services
       ↓
    Repositories
       ↓
    Models
       ↓
    PostgreSQL

Pydantic schemas define API input and output contracts.

### Responsibilities

#### Routes

Routes are responsible for:

- HTTP endpoints
- Request validation
- Dependency injection
- HTTP status codes
- HTTP error responses
- Returning API responses

Routes should remain thin.

#### Services

Services are responsible for:

- Business logic
- Validation involving multiple domain objects
- Application rules
- Coordinating repositories

Business logic should generally live here rather than inside route handlers.

#### Repositories

Repositories are responsible for:

- Database queries
- Creating records
- Updating records
- Deleting records
- Retrieving records

Repositories should not contain HTTP-specific logic.

#### Models

SQLAlchemy models represent database tables and relationships.

#### Schemas

Pydantic schemas define:

- Request bodies
- Update payloads
- Response structures
- API validation

---

## Development Workflow

Development must be incremental.

For every significant change:

1. Explain what we are building.
2. Explain why it is needed.
3. Provide the Bash command needed.
4. Provide complete file contents when creating or replacing files.
5. Explain how the implementation works.
6. Run the appropriate test or verification.
7. Confirm the expected result.
8. Only then move to the next step.

The preferred development style is:

    Explain
    ↓
    Command
    ↓
    Code
    ↓
    Run
    ↓
    Verify
    ↓
    Next step

Do not make large unrelated changes in a single step.

---

## Coding Principles

Prefer:

- Clear Python
- Strong typing
- Small focused functions
- Explicit business rules
- Maintainable architecture
- Reusable components
- Testable code

Avoid:

- Unnecessary abstraction
- Over-engineering
- Clever code that is difficult to understand
- Duplicated business logic
- Large route handlers
- Raw database logic inside routes

Do not rewrite working architecture simply for stylistic reasons.

---

## Database Rules

PostgreSQL is the primary database.

All database schema changes must use Alembic.

When changing a model:

1. Inspect the existing model.
2. Inspect the existing migration history.
3. Modify the model.
4. Generate an Alembic migration.
5. Review the generated migration.
6. Apply the migration.
7. Verify the database structure.

Do not manually modify the PostgreSQL schema as a replacement for migrations.

---

## API Rules

When adding an endpoint:

1. Define the Pydantic schema.
2. Implement business logic in the service.
3. Implement persistence in the repository.
4. Add the route.
5. Handle expected domain errors.
6. Test success cases.
7. Test important failure cases.

Use appropriate HTTP status codes.

Expected domain errors should be translated into HTTP errors at the route layer.

PATCH endpoints must support partial updates.

Only fields actually supplied by the client should be modified.

---

## Current Domain

The backend contains the following resources and domain models:

### Portfolio
Root portfolio entity holding developer personal and profile metadata.

### Project
Projects belonging to portfolios (`project.portfolio_id -> portfolio.id`), supporting an `is_featured` flag.

### Portfolio Section
Custom narrative sections belonging to portfolios (`portfolio_section.portfolio_id -> portfolio.id`).

### Skill
Skills categorized and ordered by position belonging to portfolios (`skill.portfolio_id -> portfolio.id`).

### Experience
Work history items belonging to portfolios (`experience.portfolio_id -> portfolio.id`).

### Education
Academic history items belonging to portfolios (`education.portfolio_id -> portfolio.id`).

### Certification
Professional credentials and licenses belonging to portfolios (`certification.portfolio_id -> portfolio.id`).

### Social Link
Platform profiles and links belonging to portfolios (`social_link.portfolio_id -> portfolio.id`).

### Resume
Document references and links belonging to portfolios (`resume.portfolio_id -> portfolio.id`).

### Project Technology
Technology tags associated with individual projects (`project_technology.project_id -> project.id`).

### Project Media
Media assets and screenshots associated with individual projects (`project_media.project_id -> project.id`).

### User
System users with Argon2-hashed passwords, active status, and superuser privileges.

---

## Current Backend Functionality

The following foundation is fully implemented and tested:

- FastAPI application with root (`/`) and health (`/health`) endpoints
- PostgreSQL database engine and session management with SQLAlchemy 2.0
- Alembic database migration management (13 migrations applied)
- Portfolio CRUD (`/api/portfolios`)
- Project CRUD (`/api/projects`) with `is_featured` support
- Portfolio Sections CRUD (`/api/sections`)
- Skills CRUD (`/api/skills`)
- Experiences CRUD (`/api/experiences`)
- Education CRUD (`/api/education`)
- Certifications CRUD (`/api/certifications`)
- Social Links CRUD (`/api/social-links`)
- Resumes CRUD (`/api/resumes`)
- Project Technologies CRUD (`/api/project-technologies`)
- Project Media CRUD (`/api/project-media`)
- Public portfolio aggregated reader endpoint (`/api/public/portfolios/{slug}`)
- Argon2 password hashing and JWT access token authentication (`/api/auth/login`, `/api/auth/register`, `/api/auth/me`)
- Superuser-protected user management (`/api/users`)
- Portfolio administration overview endpoint (`/api/admin/overview`)
- Content mutation route protection via JWT authentication across all `POST`, `PATCH`, and `DELETE` endpoints
- Partial PATCH updates across all entities
- Duplicate slug conflict prevention and foreign key validation
- Automated Pytest test suite under `backend/tests/` with SQLite in-memory isolation

This foundation should be preserved and extended rather than rebuilt.

---

## Testing Requirements

Before considering a feature complete:

- Confirm the application imports successfully.
- Test the new endpoint or feature.
- Test successful behavior.
- Test important invalid-input cases.
- Test relevant database behavior.
- Confirm existing functionality still works.
- Run the automated test suite (`pytest -c pytest.ini`).

The automated test suite is maintained under `backend/tests/` and includes in-memory database isolation fixtures for reproducible testing.

---

## Git Workflow

GitHub is the source-control system for this project.

Before beginning significant work:

    git status

Understand the current working-tree state before modifying files.

After completing a logical feature:

1. Review the changes.

    git diff

2. Run relevant tests.
3. Review the final status.

    git status

4. Commit with a clear message.

Example:

    git add .
    git commit -m "feat: add portfolio section"

5. Push after the checkpoint has been verified.

    git push origin main

Never:

- Force push without explicit instruction.
- Reset or discard user changes without explicit instruction.
- Overwrite unrelated work.
- Commit secrets.

---

## Security

Never place secrets in source code.

Never commit:

- API keys
- Passwords
- Database credentials
- Access tokens
- Private SSH keys
- .env files containing secrets

Use environment variables and .env for local configuration.

Confirm .gitignore protects sensitive files before committing.

---

## Change Discipline

Before modifying a file:

1. Inspect the existing file.
2. Understand what it currently does.
3. Check its imports and callers.
4. Identify the smallest required change.
5. Make the change.
6. Verify it.

Do not modify unrelated files simply because they could be improved.

Do not introduce a new dependency unless it provides clear value.

---

## Architecture Growth

The backend has progressed through its planned foundation and domain milestones.

### Completed Milestones
- [x] Portfolio Sections CRUD
- [x] Skills CRUD
- [x] Experience CRUD
- [x] Education CRUD
- [x] Certifications CRUD
- [x] Social Links CRUD
- [x] Resume/CV CRUD
- [x] Project Technologies CRUD
- [x] Featured Projects support
- [x] Project Media CRUD
- [x] Public Portfolio aggregation endpoint (`/api/public/portfolios/{slug}`)
- [x] User Authentication (Argon2 + JWT tokens)
- [x] Automated Pytest test suite with isolated SQLite in-memory fixtures (32 test cases)
- [x] Docker configuration and multi-container orchestration (`Dockerfile` + `docker-compose.yml`)
- [x] Public contact inquiry endpoint (`POST /api/contact`)
- [x] React frontend presentation with architectural surface treatment (high-contrast orange & black palette, ambient radial glows, masked grid, tactile grain, hairline borders, marquee ticker, project detail modal, search/filtering, and contact workflow)
- [x] OAuth2 form-compatible token endpoint (`POST /api/auth/token`) and Starlette CORS middleware

### Upcoming Architecture & Implementation Priorities
1. **Administrative Content Management Dashboard**
   - Administrative UI dashboard for managing portfolio sections, projects, media, and credentials
   - S3 / cloud storage multipart media and resume document upload pipeline

New features should fit naturally into the existing architecture.
Do not build all future features prematurely.

---

## Product Direction

Portfolio Engine should eventually allow portfolio content to be managed independently from the frontend presentation.

The long-term concept is:

    Portfolio Data
         ↓
    Portfolio Engine API
         ↓
    Frontend
         ↓
    Public Portfolio

This separation should make it possible to change the frontend design without rebuilding portfolio content.

---

## Communication

When assisting with this project:

- Explain technical concepts clearly.
- Do not assume advanced knowledge.
- Distinguish clearly between Bash commands and file code.
- Explain why a change is being made.
- State what successful output should look like.
- Work one meaningful checkpoint at a time.

The developer should understand the system rather than blindly copy commands.

---

## Primary Goal

Build Portfolio Engine into a professional, maintainable software project that can serve as a strong demonstration of engineering ability.

Priorities:

1. Correctness
2. Maintainability
3. Clear architecture
4. Testability
5. Security
6. Professional API design
7. Extensibility

Avoid unnecessary complexity.

