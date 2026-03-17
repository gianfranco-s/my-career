from my_career.config import RESUME_PATH, ROLES_PATH
from my_career.domain.resume_loader import build_resume
from my_career.domain.models import FullResume
from my_career.domain.filters import filter_work_experiences, get_filters

def get_resume() -> FullResume:
    return build_resume(RESUME_PATH)


def get_predefined_roles() -> list[str]:
    all_filters = get_filters(ROLES_PATH)
    return list(all_filters.keys())


def get_resume_with_filtered_work_exp(resume: FullResume, role: str) -> FullResume:
    include = get_filters(ROLES_PATH).get(role)
    if include is None:
        raise ValueError(f"{role=} does not exist in predefined roles")
    return filter_work_experiences(resume, include)


def get_resume_filters(role: str) -> list[str]:
    all_filters = get_filters(ROLES_PATH)
    return all_filters.get(role)
