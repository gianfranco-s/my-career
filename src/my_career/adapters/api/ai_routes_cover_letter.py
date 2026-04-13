from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from my_career.domain.models import JobDescription
from my_career.use_cases.ai_cover_letter import AiCoverLetterService
from my_career.ports.cover_letter_boundary import CoverLetterBoundary

router = APIRouter(tags=["cover-letter-ai"])


class JobDescriptionBody(BaseModel):
    job_description: str


@router.post("/tailor")
def tailor_cover_letter(request: Request, body: JobDescriptionBody):
    cover_letter_service: CoverLetterBoundary = request.app.state.cover_letter_service
    letter = cover_letter_service.get_cover_letter()
    service: AiCoverLetterService = request.app.state.ai_cover_letter_service
    return service.tailor_cover_letter(letter, JobDescription(text=body.job_description))


@router.post("/tailor/pdf")
def tailor_cover_letter_pdf(request: Request, body: JobDescriptionBody):
    cover_letter_service: CoverLetterBoundary = request.app.state.cover_letter_service
    letter = cover_letter_service.get_cover_letter()
    service: AiCoverLetterService = request.app.state.ai_cover_letter_service
    pdf_bytes = service.tailor_cover_letter_pdf(letter, JobDescription(text=body.job_description))
    return Response(content=pdf_bytes, media_type="application/pdf")
