from unittest.mock import MagicMock

import pytest

from my_career.use_cases.ai_resume import AiResumeService


@pytest.fixture
def resume_service(full_resume):
    svc = MagicMock()
    svc.export_resume_pdf.return_value = b"%PDF-tailored"
    return svc


@pytest.fixture
def openai_client():
    return MagicMock()


@pytest.fixture
def ai_resume_service(resume_service, openai_client):
    return AiResumeService(resume_service=resume_service, openai_client=openai_client)


def test_tailor_resume_calls_tailor_with_given_resume(ai_resume_service, full_resume, job_description, mocker):
    tailored = full_resume
    mock_tailor = mocker.patch("my_career.use_cases.ai_resume.OpenAiTailor")
    mock_tailor.return_value.get_tailored_resume.return_value = tailored

    result = ai_resume_service.tailor_resume(full_resume, job_description)

    mock_tailor.return_value.get_tailored_resume.assert_called_once_with(full_resume)
    assert result is tailored


def test_tailor_resume_pdf_exports_tailored_result(ai_resume_service, full_resume, job_description, resume_service, mocker):
    tailored = full_resume
    mock_tailor = mocker.patch("my_career.use_cases.ai_resume.OpenAiTailor")
    mock_tailor.return_value.get_tailored_resume.return_value = tailored

    result = ai_resume_service.tailor_resume_pdf(full_resume, job_description)

    resume_service.export_resume_pdf.assert_called_once_with(tailored)
    assert result == b"%PDF-tailored"
