"""Unit tests for ResumeService filtering logic."""
from unittest.mock import MagicMock

import pytest

from my_career.domain.filters import (
    filter_education,
    filter_sections,
    filter_skills,
    filter_work_experiences,
)
from my_career.use_cases.resume import ResumeService


@pytest.fixture
def pdf_exporter():
    exporter = MagicMock()
    exporter.export_to_bytes.return_value = b"%PDF"
    return exporter


@pytest.fixture
def predefined_roles():
    return {
        "backend": {
            "include": ["Acme Corp"],
            "include_education": ["CS"],
            "include_sections": ["work", "education", "skills"],
            "max_bullets": 2,
            "max_skills": None,
        },
        "all-roles": {
            "include": [],
            "include_education": [],
            "include_sections": [],
            "max_bullets": None,
            "max_skills": None,
        },
    }


@pytest.fixture
def service(full_resume, predefined_roles, pdf_exporter):
    return ResumeService(
        resume=full_resume,
        predefined_roles=predefined_roles,
        pdf_exporter=pdf_exporter,
    )


# ---------------------------------------------------------------------------
# ResumeService
# ---------------------------------------------------------------------------

def test_get_resume_returns_full_resume(service, full_resume):
    assert service.get_resume() == full_resume


def test_get_available_roles(service):
    assert set(service.get_available_roles()) == {"backend", "all-roles"}


def test_get_filtered_resume_raises_for_unknown_role(service):
    with pytest.raises(ValueError, match="does not exist in predefined roles"):
        service.get_filtered_resume("nonexistent")


def test_get_filtered_resume_filters_work_by_name(service):
    result = service.get_filtered_resume("backend")
    assert len(result.work) == 1
    assert result.work[0].name == "Acme Corp"


def test_get_filtered_resume_filters_education_by_area(service):
    result = service.get_filtered_resume("backend")
    assert len(result.education) == 1
    assert result.education[0].area == "CS"


def test_get_filtered_resume_excludes_sections_not_in_include_sections(service):
    result = service.get_filtered_resume("backend")
    assert result.certificates == []
    assert result.languages == []
    assert result.interests == []


def test_get_filtered_resume_respects_max_bullets(service):
    result = service.get_filtered_resume("backend")
    assert len(result.work[0].highlights) == 2


def test_export_pdf_delegates_to_exporter(service, full_resume, pdf_exporter):
    result = service.export_pdf()
    pdf_exporter.export_to_bytes.assert_called_once_with(full_resume)
    assert result == b"%PDF"


def test_export_resume_pdf_accepts_explicit_resume(service, full_resume, pdf_exporter):
    result = service.export_resume_pdf(full_resume)
    pdf_exporter.export_to_bytes.assert_called_once_with(full_resume)
    assert result == b"%PDF"


# ---------------------------------------------------------------------------
# filter_work_experiences
# ---------------------------------------------------------------------------

def test_filter_work_no_include_returns_all(full_resume):
    result = filter_work_experiences(full_resume, include=[])
    assert result.work == full_resume.work


def test_filter_work_by_name(full_resume):
    result = filter_work_experiences(full_resume, include=["Acme Corp"])
    assert len(result.work) == 1
    assert result.work[0].name == "Acme Corp"


def test_filter_work_max_bullets_int(full_resume):
    result = filter_work_experiences(full_resume, include=[], max_bullets=1)
    for we in result.work:
        assert len(we.highlights) <= 1


def test_filter_work_max_bullets_zero_excludes_entry(full_resume):
    result = filter_work_experiences(full_resume, include=["Acme Corp"], max_bullets=0)
    assert result.work == []


def test_filter_work_max_bullets_dict_per_company(full_resume):
    result = filter_work_experiences(full_resume, include=[], max_bullets={"Acme Corp": 1, "Beta Inc": 2})
    acme = next(w for w in result.work if w.name == "Acme Corp")
    beta = next(w for w in result.work if w.name == "Beta Inc")
    assert len(acme.highlights) == 1
    assert len(beta.highlights) == 2


# ---------------------------------------------------------------------------
# filter_education
# ---------------------------------------------------------------------------

def test_filter_education_no_include_returns_all(full_resume):
    result = filter_education(full_resume, include=[])
    assert result.education == full_resume.education


def test_filter_education_by_area(full_resume):
    result = filter_education(full_resume, include=["CS"])
    assert len(result.education) == 1
    assert result.education[0].area == "CS"


# ---------------------------------------------------------------------------
# filter_sections
# ---------------------------------------------------------------------------

def test_filter_sections_no_include_returns_unchanged(full_resume):
    result = filter_sections(full_resume, include_sections=[])
    assert result == full_resume


def test_filter_sections_excludes_unlisted_sections(full_resume):
    result = filter_sections(full_resume, include_sections=["work", "education"])
    assert result.certificates == []
    assert result.skills == []


def test_filter_sections_raises_for_unknown_section(full_resume):
    with pytest.raises(ValueError, match="Unknown sections"):
        filter_sections(full_resume, include_sections=["not-a-section"])


# ---------------------------------------------------------------------------
# filter_skills
# ---------------------------------------------------------------------------

def test_filter_skills_none_returns_unchanged(full_resume):
    result = filter_skills(full_resume, max_items=None)
    assert result == full_resume


def test_filter_skills_int_truncates_keywords(full_resume):
    result = filter_skills(full_resume, max_items=1)
    for skill in result.skills:
        assert len(skill.keywords) <= 1


def test_filter_skills_dict_per_skill(full_resume):
    result = filter_skills(full_resume, max_items={"Backend": 2, "Infra": 1})
    backend = next(s for s in result.skills if s.name == "Backend")
    infra = next(s for s in result.skills if s.name == "Infra")
    assert len(backend.keywords) == 2
    assert len(infra.keywords) == 1
