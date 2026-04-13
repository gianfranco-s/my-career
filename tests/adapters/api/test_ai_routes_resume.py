from unittest.mock import MagicMock
from dataclasses import asdict

import pytest


JD_BODY = {"job_description": "Looking for a senior Python engineer."}


@pytest.fixture(autouse=True)
def setup_state(test_app, full_resume):
    mock_resume_service = MagicMock()
    mock_resume_service.get_resume.return_value = full_resume
    mock_resume_service.get_filtered_resume.return_value = full_resume

    mock_ai_service = MagicMock()
    mock_ai_service.tailor_resume.return_value = full_resume
    mock_ai_service.tailor_resume_pdf.return_value = b"%PDF-tailored"

    test_app.state.resume_service = mock_resume_service
    test_app.state.ai_resume_service = mock_ai_service


def test_tailor_resume_returns_200(client):
    response = client.post("/v1/resume/tailor", json=JD_BODY)
    assert response.status_code == 200


def test_tailor_resume_passes_full_resume_when_no_role(test_app, client, full_resume):
    client.post("/v1/resume/tailor", json=JD_BODY)
    test_app.state.resume_service.get_resume.assert_called_once()
    test_app.state.resume_service.get_filtered_resume.assert_not_called()


def test_tailor_resume_passes_filtered_resume_when_role_given(test_app, client):
    client.post("/v1/resume/tailor", json=JD_BODY, params={"role": "backend"})
    test_app.state.resume_service.get_filtered_resume.assert_called_once_with("backend")
    test_app.state.resume_service.get_resume.assert_not_called()


def test_tailor_resume_pdf_returns_pdf_content_type(client):
    response = client.post("/v1/resume/tailor/pdf", json=JD_BODY)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_tailor_resume_pdf_returns_pdf_bytes(client):
    response = client.post("/v1/resume/tailor/pdf", json=JD_BODY)
    assert response.content == b"%PDF-tailored"
