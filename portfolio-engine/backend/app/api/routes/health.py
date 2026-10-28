from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    return {
        "status": "healthy",
    }
