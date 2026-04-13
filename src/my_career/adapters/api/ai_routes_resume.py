from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from my_career.domain.models import JobDescription
from my_career.use_cases.ai_resume import AiResumeService

router = APIRouter(tags=["resume-ai"])


class JobDescriptionBody(BaseModel):
    text: str


@router.post("/tailor")
def tailor_resume(request: Request, body: JobDescriptionBody, role: str | None = None):
    service: AiResumeService = request.app.state.ai_resume_service
    return service.tailor_resume(JobDescription(text=body.text), role)


@router.post("/tailor/pdf")
def tailor_resume_pdf(request: Request, body: JobDescriptionBody, role: str | None = None):
    service: AiResumeService = request.app.state.ai_resume_service
    pdf_bytes = service.tailor_resume_pdf(JobDescription(text=body.text), role)
    return Response(content=pdf_bytes, media_type="application/pdf")
