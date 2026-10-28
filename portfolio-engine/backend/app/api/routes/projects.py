from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.core.products import PRODUCTS
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project import (
    PortfolioNotFoundError,
    ProjectService,
    ProjectSlugExistsError,
)


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)


@router.get(
    "/showcase",
    response_model=list[dict],
)
def get_showcase():
    """Retrieve curated product showcase entries without proprietary details."""
    return PRODUCTS


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    try:
        return service.create(data)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except ProjectSlugExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def get_projects(
    db: Session = Depends(get_db),
):
    service = ProjectService(db)
    return service.get_all()


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=list[ProjectResponse],
)
def get_projects_by_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
):
    service = ProjectService(db)
    return service.get_by_portfolio_id(portfolio_id)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    service = ProjectService(db)
    project = service.get_by_id(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    dependencies=[Depends(get_current_user)],
)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    try:
        project = service.update(project_id, data)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except ProjectSlugExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    if not service.delete(project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
