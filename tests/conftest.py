import time

import jwt
import pytest
from fastapi import FastAPI, Security
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient

from my_career.adapters.api.ai_routes_resume import router as ai_resume_router
from my_career.adapters.api.ai_routes_cover_letter import router as ai_cover_letter_router
from my_career.adapters.api.routes_resume import router as resume_router
from my_career.adapters.api.routes_cover_letter import router as cover_letter_router
from my_career.adapters.api.auth import require_auth
from my_career.adapters.api.error_handlers import (
    validation_error_handler,
    value_error_handler,
    unhandled_error_handler,
)
from my_career.domain.models import (
    CoverLetter,
    Education,
    Certificate,
    FullResume,
    JobDescription,
    Language,
    Location,
    PersonalInterest,
    Project,
    ResumeBasics,
    Skill,
    SocialMediaProfile,
    WorkExperience,
)

TEST_JWT_SECRET = "test-secret-long-enough-for-hmac-sha256-requirement"


# ---------------------------------------------------------------------------
# Domain fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def location():
    return Location(countryCode="US", region="CA", city="San Francisco")


@pytest.fixture
def work_experience(location):
    return WorkExperience(
        name="Acme Corp",
        position="Software Engineer",
        startDate="2020-01",
        summary="Built things",
        isRemote=True,
        location=location,
        highlights=["Shipped feature X", "Shipped feature Y", "Shipped feature Z"],
        techHighlights=["Python", "FastAPI"],
    )


@pytest.fixture
def another_work_experience(location):
    return WorkExperience(
        name="Beta Inc",
        position="Senior Engineer",
        startDate="2018-01",
        endDate="2020-01",
        summary="Built more things",
        isRemote=False,
        location=location,
        highlights=["Led project A", "Led project B"],
        techHighlights=["Go", "Kubernetes"],
    )


@pytest.fixture
def full_resume(location, work_experience, another_work_experience):
    basics = ResumeBasics(
        name="Jane Doe",
        label="Engineer",
        image="",
        email="jane@example.com",
        phone="+1 555 0000",
        url="https://jane.dev",
        summary="A great engineer",
        location=location,
        profiles=[SocialMediaProfile(network="LinkedIn", url="https://linkedin.com/in/jane")],
    )
    return FullResume(
        basics=basics,
        work=[work_experience, another_work_experience],
        education=[
            Education(institution="MIT", area="CS", startDate="2016-09", endDate="2020-05"),
            Education(institution="Stanford", area="Math", startDate="2014-09", endDate="2016-05"),
        ],
        certificates=[Certificate(name="AWS SAA", date="2022-01", issuer="Amazon", url="https://aws.amazon.com")],
        languages=[Language(language="English", fluency="Native")],
        interests=[PersonalInterest(name="OSS", summary="Open source contributor")],
        skills=[
            Skill(name="Backend", keywords=["Python", "FastAPI", "Go"]),
            Skill(name="Infra", keywords=["Docker", "Kubernetes"]),
        ],
        projects=[Project(name="My Project", startDate="2021-01", description="Cool project", highlights=["Did X"])],
    )


@pytest.fixture
def cover_letter():
    return CoverLetter(
        date="2026-04-13",
        contact_title="Hiring Manager",
        contact_company="Acme Corp",
        text=["Dear Hiring Manager,", "I am excited to apply."],
        sender_signature="Jane Doe",
        sender_email="jane@example.com",
    )


@pytest.fixture
def job_description():
    return JobDescription(text="We are looking for a senior Python engineer.")


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------

def make_token(secret: str = TEST_JWT_SECRET, expired: bool = False) -> str:
    exp = time.time() + (-10 if expired else 3600)
    return jwt.encode({"exp": exp}, secret, algorithm="HS256")


@pytest.fixture
def valid_token():
    return make_token()


@pytest.fixture
def auth_headers(valid_token):
    return {"Authorization": f"Bearer {valid_token}"}


# ---------------------------------------------------------------------------
# AI test app — auth bypassed, state injected per test
# ---------------------------------------------------------------------------

def _create_ai_test_app() -> FastAPI:
    app = FastAPI()
    app.dependency_overrides[require_auth] = lambda: None
    app.include_router(ai_resume_router, prefix="/v1/resume")
    app.include_router(ai_cover_letter_router, prefix="/v1/cover-letter")
    return app


@pytest.fixture
def test_app():
    return _create_ai_test_app()


@pytest.fixture
def client(test_app):
    return TestClient(test_app)


# ---------------------------------------------------------------------------
# Protected test app — real auth + existing routes + error handlers
# ---------------------------------------------------------------------------

def _create_protected_app() -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
    app.include_router(resume_router, prefix="/v1/resume", dependencies=[Security(require_auth)])
    app.include_router(cover_letter_router, prefix="/v1/cover-letter", dependencies=[Security(require_auth)])
    return app


@pytest.fixture
def protected_app():
    return _create_protected_app()


@pytest.fixture
def protected_client(protected_app):
    return TestClient(protected_app, raise_server_exceptions=False)
