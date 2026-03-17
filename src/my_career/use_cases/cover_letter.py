from dataclasses import replace, fields
from my_career.config import LETTER_PATH
from my_career.domain.letter_loader import build_letter
from my_career.domain.models import CoverLetter
from my_career.ports.exporter import CoverLetterExporter


def load_cover_letter() -> CoverLetter:
    return build_letter(LETTER_PATH)


class CoverLetterService:
    def __init__(self, cover_letter: CoverLetter, pdf_exporter: CoverLetterExporter):
        self.__cover_letter = cover_letter
        self.__pdf_exporter = pdf_exporter

    def get_cover_letter(self) -> CoverLetter:
        return self.__cover_letter

    def get_updated_cover_letter(self, **kwargs) -> CoverLetter:
        valid_fields = {f.name for f in fields(CoverLetter)}
        invalid = set(kwargs) - valid_fields
        if invalid:
            raise ValueError(f"Invalid fields: {invalid}. Valid fields: {valid_fields}")
        return replace(self.__cover_letter, **kwargs)

    def export_pdf(self, **kwargs) -> bytes:
        letter = self.get_updated_cover_letter(**kwargs) if kwargs else self.__cover_letter
        return self.__pdf_exporter.export_to_bytes(letter)
