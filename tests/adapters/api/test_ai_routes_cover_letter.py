from unittest.mock import MagicMock

import pytest


JD_BODY = {"job_description": "Looking for a senior Python engineer."}


@pytest.fixture(autouse=True)
def setup_state(test_app, cover_letter):
    mock_cover_letter_service = MagicMock()
    mock_cover_letter_service.get_cover_letter.return_value = cover_letter
    mock_cover_letter_service.get_updated_cover_letter.return_value = cover_letter

    mock_ai_service = MagicMock()
    mock_ai_service.tailor_cover_letter.return_value = cover_letter
    mock_ai_service.tailor_cover_letter_pdf.return_value = b"%PDF-letter"

    test_app.state.cover_letter_service = mock_cover_letter_service
    test_app.state.ai_cover_letter_service = mock_ai_service


def test_tailor_cover_letter_returns_200(client):
    response = client.post("/v1/cover-letter/tailor", json=JD_BODY)
    assert response.status_code == 200


def test_tailor_cover_letter_uses_base_letter_when_no_overrides(test_app, client):
    client.post("/v1/cover-letter/tailor", json=JD_BODY)
    test_app.state.cover_letter_service.get_cover_letter.assert_called_once()
    test_app.state.cover_letter_service.get_updated_cover_letter.assert_not_called()


def test_tailor_cover_letter_applies_overrides(test_app, client):
    body = {**JD_BODY, "contact_company": "New Corp", "contact_name": "Alice"}
    client.post("/v1/cover-letter/tailor", json=body)
    test_app.state.cover_letter_service.get_updated_cover_letter.assert_called_once_with(
        contact_company="New Corp", contact_name="Alice"
    )
    test_app.state.cover_letter_service.get_cover_letter.assert_not_called()


def test_tailor_cover_letter_pdf_returns_pdf_content_type(client):
    response = client.post("/v1/cover-letter/tailor/pdf", json=JD_BODY)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_tailor_cover_letter_pdf_returns_pdf_bytes(client):
    response = client.post("/v1/cover-letter/tailor/pdf", json=JD_BODY)
    assert response.content == b"%PDF-letter"
