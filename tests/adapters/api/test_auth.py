"""Auth enforcement tests — verify 401 is returned on protected routes."""
from unittest.mock import MagicMock

import pytest

from tests.conftest import make_token


@pytest.fixture(autouse=True)
def setup_state(protected_app, full_resume, cover_letter):
    mock_resume_service = MagicMock()
    mock_resume_service.get_resume.return_value = full_resume
    mock_cover_letter_service = MagicMock()
    mock_cover_letter_service.get_cover_letter.return_value = cover_letter
    protected_app.state.resume_service = mock_resume_service
    protected_app.state.cover_letter_service = mock_cover_letter_service


PROTECTED_ROUTES = [
    ("GET", "/v1/resume"),
    ("GET", "/v1/resume/roles"),
    ("GET", "/v1/cover-letter"),
]


@pytest.mark.parametrize("method,path", PROTECTED_ROUTES)
def test_returns_401_with_no_token(protected_client, method, path):
    response = protected_client.request(method, path)
    assert response.status_code == 401


@pytest.mark.parametrize("method,path", PROTECTED_ROUTES)
def test_returns_401_with_invalid_token(protected_client, method, path):
    headers = {"Authorization": "Bearer not-a-valid-jwt"}
    response = protected_client.request(method, path, headers=headers)
    assert response.status_code == 401


@pytest.mark.parametrize("method,path", PROTECTED_ROUTES)
def test_returns_401_with_expired_token(protected_client, method, path):
    headers = {"Authorization": f"Bearer {make_token(expired=True)}"}
    response = protected_client.request(method, path, headers=headers)
    assert response.status_code == 401


@pytest.mark.parametrize("method,path", PROTECTED_ROUTES)
def test_returns_200_with_valid_token(protected_client, auth_headers, method, path):
    response = protected_client.request(method, path, headers=auth_headers)
    assert response.status_code == 200
