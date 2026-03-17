from contextlib import asynccontextmanager

from fastapi import FastAPI

from my_career.adapters.api.routes_resume import router as resume
from my_career.adapters.api.routes_cover_letter import router as cover_letter
from my_career.adapters.pdf_exporter import ResumePdfExporter, LetterPdfExporter
from my_career.use_cases.resume import load_resume, load_filters, ResumeService
from my_career.use_cases.cover_letter import load_cover_letter, CoverLetterService
from my_career.config import RESUME_TEMPLATE_PATH, LETTER_TEMPLATE_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.resume_service = ResumeService(
        resume=load_resume(),
        predefined_roles=load_filters(),
        pdf_exporter=ResumePdfExporter(RESUME_TEMPLATE_PATH),
    )
    app.state.cover_letter_service = CoverLetterService(
        cover_letter=load_cover_letter(),
        pdf_exporter=LetterPdfExporter(LETTER_TEMPLATE_PATH),
    )

    yield


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(resume)
    app.include_router(cover_letter)
    return app


app = create_app()
