from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from my_career.ports.cover_letter_boundary import CoverLetterBoundary

router = APIRouter()


class CoverLetterOverrides(BaseModel):
    contact_title: str | None = None
    contact_company: str | None = None
    contact_name: str | None = None
    contact_address: str | None = None


@router.get("/cover-letter")
def get_cover_letter(request: Request):
    service: CoverLetterBoundary = request.app.state.cover_letter_service
    return service.get_cover_letter()


@router.patch("/cover-letter")
def update_cover_letter(request: Request, overrides: CoverLetterOverrides):
    kwargs = {k: v for k, v in overrides.model_dump().items() if v is not None}
    service: CoverLetterBoundary = request.app.state.cover_letter_service
    return service.get_updated_cover_letter(**kwargs)


@router.get("/cover-letter/pdf")
def get_cover_letter_pdf(request: Request):
    """Returns pdf at <api-root>/cover-letter/pdf"""
    service: CoverLetterBoundary = request.app.state.cover_letter_service
    return Response(content=service.export_pdf(), media_type="application/pdf")


@router.patch("/cover-letter/pdf")
def get_updated_cover_letter_pdf(request: Request, overrides: CoverLetterOverrides):
    """Returns pdf at <api-root>/cover-letter/pdf"""
    kwargs = {k: v for k, v in overrides.model_dump().items() if v is not None}
    service: CoverLetterBoundary = request.app.state.cover_letter_service
    return Response(content=service.export_pdf(**kwargs), media_type="application/pdf")
