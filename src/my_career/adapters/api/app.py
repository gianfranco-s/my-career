from contextlib import asynccontextmanager

from fastapi import FastAPI

from my_career.adapters.api.routes_resume import router as resume
from my_career.adapters.api.routes_cover_letter import router as cover_letter
from my_career.use_cases.resume import get_resume
from my_career.use_cases.cover_letter import get_cover_letter


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cache resume and cover_letter, as they will not change during runtime
    app.state.resume = get_resume()
    app.state.cover_letter = get_cover_letter()

    yield


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(resume)
    app.include_router(cover_letter)
    return app


app = create_app()
