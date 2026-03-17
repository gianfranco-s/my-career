from typing import Protocol
from my_career.domain.models import FullResume, CoverLetter


class ResumeExporter(Protocol):
    def export(self, resume: FullResume, output_path: str) -> None: ...

class CoverLetterExporter(Protocol):
    def export(self, letter: CoverLetter, output_path: str) -> None: ...
