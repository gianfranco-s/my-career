"""Regression tests for existing cover letter routes."""
from unittest.mock import MagicMock

import pytest


@pytest.fixture(autouse=True)
def setup_state(protected_app, cover_letter):
    mock_service = MagicMock()
    mock_service.get_cover_letter.return_value = cover_letter
    mock_service.get_updated_cover_letter.return_value = cover_letter
    mock_service.export_pdf.return_value = b"%PDF-letter"
    protected_app.state.cover_letter_service = mock_service


def test_get_cover_letter_returns_data(protected_client, auth_headers):
    response = protected_client.get("/v1/cover-letter", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["contact_company"] == "Acme Corp"


def test_patch_cover_letter_applies_override(protected_client, auth_headers, protected_app):
    response = protected_client.patch(
        "/v1/cover-letter",
        headers=auth_headers,
        json={"contact_company": "New Corp"},
    )
    assert response.status_code == 200
    protected_app.state.cover_letter_service.get_updated_cover_letter.assert_called_once_with(
        contact_company="New Corp"
    )


def test_patch_cover_letter_ignores_none_fields(protected_client, auth_headers, protected_app):
    response = protected_client.patch(
        "/v1/cover-letter",
        headers=auth_headers,
        json={"contact_company": "New Corp", "contact_name": None},
    )
    assert response.status_code == 200
    call_kwargs = protected_app.state.cover_letter_service.get_updated_cover_letter.call_args.kwargs
    assert "contact_name" not in call_kwargs


def test_get_cover_letter_pdf_returns_pdf(protected_client, auth_headers):
    response = protected_client.get("/v1/cover-letter/pdf", headers=auth_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content == b"%PDF-letter"


def test_patch_cover_letter_pdf_returns_pdf(protected_client, auth_headers):
    response = protected_client.patch(
        "/v1/cover-letter/pdf",
        headers=auth_headers,
        json={"contact_company": "New Corp"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
