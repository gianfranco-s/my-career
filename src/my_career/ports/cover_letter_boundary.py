from typing import Protocol

from my_career.domain.models import CoverLetter


class CoverLetterBoundary(Protocol):
    def get_cover_letter(self) -> CoverLetter: ...
    def get_updated_cover_letter(self, **kwargs) -> CoverLetter: ...
