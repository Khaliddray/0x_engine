import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.project_media import (
    ProjectMediaCreate,
    ProjectMediaResponse,
    ProjectMediaUpdate,
)
from app.services.project_media import (
    ProjectMediaService,
    ProjectNotFoundError,
)

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
    "image/svg+xml",
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

STATIC_DIR = Path(__file__).resolve().parents[4] / "frontend" / "static"
UPLOAD_DIR = STATIC_DIR / "uploads" / "projects"

router = APIRouter(
    prefix="/api/project-media",
    tags=["Project Media"],
)


@router.post(
    "/upload",
    dependencies=[Depends(get_current_user)],
)
async def upload_project_image(
    file: UploadFile = File(...),
):
    """Upload an image file directly for a project visual preview."""
    file_ext = Path(file.filename or "").suffix.lower()
    if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file format '{file_ext}'. "
                f"Allowed formats: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}"
            ),
        )

    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported image MIME type '{file.content_type}'.",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    target_path = UPLOAD_DIR / unique_name

    size = 0
    with target_path.open("wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_FILE_SIZE:
                target_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File exceeds maximum allowed size of 10MB.",
                )
            buffer.write(chunk)

    return {
        "url": f"/static/uploads/projects/{unique_name}",
        "filename": unique_name,
        "size": size,
    }


@router.post(
    "",
    response_model=ProjectMediaResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_project_media(
    data: ProjectMediaCreate,
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)

    try:
        return service.create(data)

    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ProjectMediaResponse],
)
def get_project_media(
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)
    return service.get_all()


@router.get(
    "/project/{project_id}",
    response_model=list[ProjectMediaResponse],
)
def get_project_media_by_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)
    return service.get_by_project_id(project_id)


@router.get(
    "/{media_id}",
    response_model=ProjectMediaResponse,
)
def get_project_media_item(
    media_id: int,
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)
    media = service.get_by_id(media_id)

    if media is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project media not found",
        )

    return media


@router.patch(
    "/{media_id}",
    response_model=ProjectMediaResponse,
    dependencies=[Depends(get_current_user)],
)
def update_project_media(
    media_id: int,
    data: ProjectMediaUpdate,
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)

    try:
        media = service.update(media_id, data)

    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    if media is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project media not found",
        )

    return media


@router.delete(
    "/{media_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
def delete_project_media(
    media_id: int,
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)

    if not service.delete(media_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project media not found",
        )
