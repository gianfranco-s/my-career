from contextlib import asynccontextmanager

from fastapi import FastAPI, Security
from fastapi.exceptions import RequestValidationError
from openai import OpenAI

from my_career.adapters.api.auth import require_auth
from my_career.adapters.api.error_handlers import validation_error_handler, value_error_handler, unhandled_error_handler
from my_career.adapters.api.routes_cover_letter import router as cover_letter
from my_career.adapters.api.routes_resume import router as resume
from my_career.adapters.api.routes_health import router as health
from my_career.adapters.api.ai_routes_resume import router as ai_resume
from my_career.adapters.api.ai_routes_cover_letter import router as ai_cover_letter
from my_career.adapters.pdf_exporter import ResumePdfExporter, LetterPdfExporter
from my_career.use_cases.cover_letter import load_cover_letter, CoverLetterService
from my_career.use_cases.resume import load_resume, load_filters, ResumeService
from my_career.use_cases.ai_resume import AiResumeService
from my_career.use_cases.ai_cover_letter import AiCoverLetterService
from my_career.config import settings, openai_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.resume_service = ResumeService(
        resume=load_resume(),
        predefined_roles=load_filters(),
        pdf_exporter=ResumePdfExporter(settings.template_resume),
    )
    app.state.cover_letter_service = CoverLetterService(
        cover_letter=load_cover_letter(),
        pdf_exporter=LetterPdfExporter(settings.template_letter),
    )

    openai_client = OpenAI(api_key=openai_settings.openai_api_key.get_secret_value())
    app.state.ai_resume_service = AiResumeService(
        resume_service=app.state.resume_service,
        openai_client=openai_client,
    )
    app.state.ai_cover_letter_service = AiCoverLetterService(
        cover_letter_service=app.state.cover_letter_service,
        openai_client=openai_client,
    )

    yield


def create_app():
    app = FastAPI(lifespan=lifespan)

    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)

    app.include_router(resume, prefix="/v1/resume", dependencies=[Security(require_auth)])
    app.include_router(cover_letter, prefix="/v1/cover-letter", dependencies=[Security(require_auth)])
    app.include_router(ai_resume, prefix="/v1/resume", dependencies=[Security(require_auth)])
    app.include_router(ai_cover_letter, prefix="/v1/cover-letter", dependencies=[Security(require_auth)])
    app.include_router(health, prefix="/v1/health")
    return app


app = create_app()
