import logging
from fastapi import APIRouter, status

from app.schemas.contact import ContactInquiryCreate, ContactInquiryResponse

logger = logging.getLogger("portfolio.contact")

router = APIRouter(
    prefix="/api/contact",
    tags=["Contact"],
)


@router.post(
    "",
    response_model=ContactInquiryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a contact inquiry",
)
def submit_contact_inquiry(data: ContactInquiryCreate) -> ContactInquiryResponse:
    logger.info(
        "Received contact inquiry from %s <%s>: %s",
        data.name,
        data.email,
        data.subject,
    )
    return ContactInquiryResponse(
        success=True,
        message=f"Thank you, {data.name}. Your inquiry has been received and Yahaya Khalid will follow up shortly.",
    )
