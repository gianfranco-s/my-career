from unittest.mock import MagicMock

import pytest

from my_career.use_cases.ai_cover_letter import AiCoverLetterService


@pytest.fixture
def cover_letter_service():
    svc = MagicMock()
    svc.export_letter_pdf.return_value = b"%PDF-letter"
    return svc


@pytest.fixture
def openai_client():
    return MagicMock()


@pytest.fixture
def ai_cover_letter_service(cover_letter_service, openai_client):
    return AiCoverLetterService(cover_letter_service=cover_letter_service, openai_client=openai_client)


def test_tailor_cover_letter_calls_tailor_with_given_letter(ai_cover_letter_service, cover_letter, job_description, mocker):
    tailored = cover_letter
    mock_tailor = mocker.patch("my_career.use_cases.ai_cover_letter.OpenAiTailor")
    mock_tailor.return_value.get_tailored_letter.return_value = tailored

    result = ai_cover_letter_service.tailor_cover_letter(cover_letter, job_description)

    mock_tailor.return_value.get_tailored_letter.assert_called_once_with(cover_letter)
    assert result is tailored


def test_tailor_cover_letter_pdf_exports_tailored_result(ai_cover_letter_service, cover_letter, job_description, cover_letter_service, mocker):
    tailored = cover_letter
    mock_tailor = mocker.patch("my_career.use_cases.ai_cover_letter.OpenAiTailor")
    mock_tailor.return_value.get_tailored_letter.return_value = tailored

    result = ai_cover_letter_service.tailor_cover_letter_pdf(cover_letter, job_description)

    cover_letter_service.export_letter_pdf.assert_called_once_with(tailored)
    assert result == b"%PDF-letter"
