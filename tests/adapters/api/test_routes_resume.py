"""Regression tests for existing resume routes."""
from unittest.mock import MagicMock

import pytest


@pytest.fixture(autouse=True)
def setup_state(protected_app, full_resume):
    mock_service = MagicMock()
    mock_service.get_resume.return_value = full_resume
    mock_service.get_available_roles.return_value = ["backend", "frontend"]
    mock_service.get_filters_for_role.return_value = {"include": ["Acme Corp"]}
    mock_service.get_filtered_resume.return_value = full_resume
    mock_service.export_pdf.return_value = b"%PDF"
    protected_app.state.resume_service = mock_service


def test_get_resume_returns_basics(protected_client, auth_headers):
    response = protected_client.get("/v1/resume", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["basics"]["name"] == "Jane Doe"


def test_get_roles_returns_list(protected_client, auth_headers):
    response = protected_client.get("/v1/resume/roles", headers=auth_headers)
    assert response.status_code == 200
    assert "backend" in response.json()


def test_get_filters_for_role(protected_client, auth_headers):
    response = protected_client.get("/v1/resume/filters-for-role", headers=auth_headers, params={"role": "backend"})
    assert response.status_code == 200


def test_get_filtered_resume(protected_client, auth_headers):
    response = protected_client.get("/v1/resume/filtered", headers=auth_headers, params={"role": "backend"})
    assert response.status_code == 200
    assert response.json()["basics"]["name"] == "Jane Doe"


def test_get_resume_pdf_returns_pdf(protected_client, auth_headers):
    response = protected_client.get("/v1/resume/pdf", headers=auth_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content == b"%PDF"


def test_get_filtered_resume_unknown_role_returns_400(protected_client, auth_headers, protected_app):
    protected_app.state.resume_service.get_filtered_resume.side_effect = ValueError("role='bad' does not exist in predefined roles")
    response = protected_client.get("/v1/resume/filtered", headers=auth_headers, params={"role": "bad"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "BAD_REQUEST"
