from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from my_career.domain.models import JobDescription
from my_career.use_cases.ai_cover_letter import AiCoverLetterService

router = APIRouter(tags=["cover-letter-ai"])


class JobDescriptionBody(BaseModel):
    text: str


@router.post("/tailor")
def tailor_cover_letter(request: Request, body: JobDescriptionBody):
    service: AiCoverLetterService = request.app.state.ai_cover_letter_service
    return service.tailor_cover_letter(JobDescription(text=body.text))


@router.post("/tailor/pdf")
def tailor_cover_letter_pdf(request: Request, body: JobDescriptionBody):
    service: AiCoverLetterService = request.app.state.ai_cover_letter_service
    pdf_bytes = service.tailor_cover_letter_pdf(JobDescription(text=body.text))
    return Response(content=pdf_bytes, media_type="application/pdf")
