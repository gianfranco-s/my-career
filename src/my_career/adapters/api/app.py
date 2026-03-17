from contextlib import asynccontextmanager

from fastapi import FastAPI

from my_career.adapters.api.routes_resume import router as resume
from my_career.adapters.api.routes_cover_letter import router as cover_letter
from my_career.use_cases.resume import load_resume, load_filters, ResumeService
from my_career.use_cases.cover_letter import load_cover_letter, CoverLetterService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cache resume and cover_letter, as they will not change during runtime
    app.state.resume_service = ResumeService(load_resume(), load_filters())
    app.state.cover_letter_service = CoverLetterService(load_cover_letter())

    yield


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(resume)
    app.include_router(cover_letter)
    return app


app = create_app()
