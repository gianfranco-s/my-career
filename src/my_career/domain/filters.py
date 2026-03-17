import json
from dataclasses import replace

from my_career.domain.models import WorkExperience, FullResume


def get_filters(filename: str) -> dict:

    with open(filename, "r") as f:
        raw_roles = json.load(f)

    roles = dict()

    for r in raw_roles:
        role_name = r.get("role")
        work_experiences_names = r.get("include")
        roles[role_name] = work_experiences_names

    return roles


def filter_work_experiences(resume: FullResume, include: list[str]) -> FullResume:
    if len(include) < 1:
        raise ValueError("include cannot be empty")

    full_we: WorkExperience = resume.work
    filtered_work_experiences = [we for we in full_we if we.name in include]
    return replace(resume, work=filtered_work_experiences)
