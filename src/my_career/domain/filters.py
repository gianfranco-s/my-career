import json
from typing import Iterable

from domain.models import WorkExperience


def get_filters(filename: str) -> dict:

    with open(filename, "r") as f:
        raw_roles = json.load(f)

    roles = dict()

    for r in raw_roles:
        role_name = r.get("role")
        work_experiences_names = r.get("include")
        roles[role_name] = work_experiences_names

    return roles


def filter_work_experiences(work_experiences: list[WorkExperience], include: Iterable) -> list[WorkExperience]:
    if len(include) < 1:
        return work_experiences
    
    return [we for we in work_experiences if we.name in include]
