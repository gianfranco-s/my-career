import json
from dataclasses import replace

from my_career.domain.models import WorkExperience, FullResume

FILTERABLE_SECTIONS = {"work", "education", "certificates", "languages", "interests", "skills", "projects"}


def get_filters(filename: str) -> dict:
    with open(filename, "r") as f:
        raw_roles = json.load(f)

    roles = dict()

    for r in raw_roles:
        role_name = r.get("role")
        roles[role_name] = {
            "include": r.get("include", []),
            "include_education": r.get("include_education", []),
            "include_sections": r.get("include_sections", []),
        }

    return roles


def filter_work_experiences(resume: FullResume, include: list[str]) -> FullResume:
    if not include:
        return resume
    filtered = [we for we in resume.work if we.name in include]
    return replace(resume, work=filtered)


def filter_education(resume: FullResume, include: list[str]) -> FullResume:
    if not include:
        return resume
    filtered = [edu for edu in resume.education if edu.area in include]
    return replace(resume, education=filtered)


def filter_sections(resume: FullResume, include_sections: list[str]) -> FullResume:
    if not include_sections:
        return resume
    unknown = set(include_sections) - FILTERABLE_SECTIONS
    if unknown:
        raise ValueError(f"Unknown sections: {unknown}. Valid options: {FILTERABLE_SECTIONS}")
    overrides = {
        section: [] if getattr(resume, section) is not None else None
        for section in FILTERABLE_SECTIONS
        if section not in include_sections
    }
    return replace(resume, **overrides)
