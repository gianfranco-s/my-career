from my_career.config import settings
from my_career.domain.resume_loader import build_resume
from my_career.domain.models import FullResume
from my_career.domain.filters import filter_work_experiences, get_filters
from my_career.ports.exporter import ResumeExporter


def load_resume() -> FullResume:
    return build_resume(settings.source_resume)

def load_filters() -> dict:
    return get_filters(settings.source_roles)


class ResumeService:
    def __init__(self, resume: FullResume, predefined_roles: dict, pdf_exporter: ResumeExporter):
        self.__resume = resume
        self.__all_filters = predefined_roles
        self.__pdf_exporter = pdf_exporter

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

    def export_pdf(self, role: str | None = None) -> bytes:
        resume = self.get_filtered_resume(role) if role else self.__resume
        return self.__pdf_exporter.export_to_bytes(resume)
