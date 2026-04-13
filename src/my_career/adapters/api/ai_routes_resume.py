from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from my_career.domain.models import JobDescription
from my_career.use_cases.ai_resume import AiResumeService
from my_career.ports.resume_boundary import ResumeBoundary

router = APIRouter(tags=["resume-ai"])


class JobDescriptionBody(BaseModel):
    job_description: str


@router.post("/tailor")
def tailor_resume(request: Request, body: JobDescriptionBody, role: str | None = None):
    resume_service: ResumeBoundary = request.app.state.resume_service
    resume = resume_service.get_filtered_resume(role) if role else resume_service.get_resume()
    service: AiResumeService = request.app.state.ai_resume_service
    return service.tailor_resume(resume, JobDescription(text=body.job_description))


@router.post("/tailor/pdf")
def tailor_resume_pdf(request: Request, body: JobDescriptionBody, role: str | None = None):
    resume_service: ResumeBoundary = request.app.state.resume_service
    resume = resume_service.get_filtered_resume(role) if role else resume_service.get_resume()
    service: AiResumeService = request.app.state.ai_resume_service
    pdf_bytes = service.tailor_resume_pdf(resume, JobDescription(text=body.job_description))
    return Response(content=pdf_bytes, media_type="application/pdf")
