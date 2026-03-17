from my_career.config import RESUME_PATH, ROLES_PATH
from my_career.domain.resume_loader import build_resume
from my_career.domain.models import FullResume
from my_career.domain.filters import filter_work_experiences, get_filters

def load_resume() -> FullResume:
    return build_resume(RESUME_PATH)

def load_filters() -> dict:
    return get_filters(ROLES_PATH)


class ResumeService:
    def __init__(self, resume: FullResume, predefined_roles: dict):
        self.__resume = resume
        self.__all_filters = predefined_roles

    def get_resume(self) -> FullResume:
        return self.__resume

    def get_available_roles(self) -> list[str]:
        return list(self.__all_filters.keys())

    def get_filtered_resume(self, role: str) -> FullResume:
        include = self.__all_filters.get(role)
        if include is None:
            raise ValueError(f"{role=} does not exist in predefined roles")
        return filter_work_experiences(self.__resume, include)

    def get_filters_for_role(self, role: str) -> list[str]:
        include = self.__all_filters.get(role)
        if include is None:
            raise ValueError(f"{role=} does not exist in predefined roles")
        return include
