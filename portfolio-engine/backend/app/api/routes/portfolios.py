from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse,
    PortfolioUpdate,
)
from app.services.portfolio import (
    PortfolioService,
    PortfolioSlugExistsError,
)


router = APIRouter(
    prefix="/api/portfolios",
    tags=["Portfolios"],
)


@router.post(
    "",
    response_model=PortfolioResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_portfolio(
    data: PortfolioCreate,
    db: Session = Depends(get_db),
):
    service = PortfolioService(db)

    try:
        return service.create(data)
    except PortfolioSlugExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[PortfolioResponse],
)
def get_portfolios(
    db: Session = Depends(get_db),
):
    service = PortfolioService(db)
    return service.get_all()


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
):
    service = PortfolioService(db)
    portfolio = service.get_by_id(portfolio_id)

    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    return portfolio


@router.patch(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
    dependencies=[Depends(get_current_user)],
)
def update_portfolio(
    portfolio_id: int,
    data: PortfolioUpdate,
    db: Session = Depends(get_db),
):
    service = PortfolioService(db)

    try:
        portfolio = service.update(portfolio_id, data)
    except PortfolioSlugExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    return portfolio


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
):
    service = PortfolioService(db)

    if not service.delete(portfolio_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
