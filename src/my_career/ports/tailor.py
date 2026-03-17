from typing import Protocol

from my_career.domain.models import FullResume, CoverLetter


class ContentTailor(Protocol):
    def get_tailored_resume(self, content: FullResume, dry_run: bool = False) -> FullResume | None: ...
    def get_tailored_letter(self, content: CoverLetter, dry_run: bool = False) -> CoverLetter | None: ...
