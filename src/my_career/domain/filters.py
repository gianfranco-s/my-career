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
            "max_bullets": r.get("max_bullets", None),
            "max_skills": r.get("max_skills", None),
        }

    return roles


def filter_work_experiences(resume: FullResume, include: list[str], max_bullets: int | dict | None = None) -> FullResume:
    if not include:
        work = resume.work
    else:
        work = [we for we in resume.work if we.name in include]
    if max_bullets is not None:
        if isinstance(max_bullets, int):
            work = [we for we in work if max_bullets != 0]
            work = [replace(we, highlights=we.highlights[:max_bullets or None]) for we in work]
        elif isinstance(max_bullets, dict):
            work = [we for we in work if max_bullets.get(we.name, 1) != 0]
            work = [replace(we, highlights=we.highlights[:max_bullets[we.name]]) if we.name in max_bullets else we for we in work]
    return replace(resume, work=work)


def filter_skills(resume: FullResume, max_items: int | dict | None = None) -> FullResume:
    if max_items is None:
        return resume
    if isinstance(max_items, int):
        skills = [replace(s, keywords=s.keywords[:max_items]) for s in resume.skills if max_items != 0]
    elif isinstance(max_items, dict):
        skills = [s for s in resume.skills if max_items.get(s.name, 1) != 0]
        skills = [replace(s, keywords=s.keywords[:max_items[s.name]]) if s.name in max_items else s for s in skills]
    return replace(resume, skills=skills)


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
