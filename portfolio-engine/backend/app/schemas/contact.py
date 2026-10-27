from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field


class ContactInquiryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    subject: str = Field(min_length=2, max_length=200)
    message: str = Field(min_length=5, max_length=5000)


class ContactInquiryResponse(BaseModel):
    success: bool = True
    message: str
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
