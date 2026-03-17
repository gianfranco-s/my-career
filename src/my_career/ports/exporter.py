from typing import Protocol
from my_career.domain.models import FullResume


class ResumeExporter(Protocol):
    def export(self, resume: FullResume, output_path: str) -> None: ...
