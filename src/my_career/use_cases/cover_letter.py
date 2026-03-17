from dataclasses import replace, fields
from my_career.config import LETTER_PATH
from my_career.domain.letter_loader import build_letter
from my_career.domain.models import CoverLetter


def get_cover_letter() -> CoverLetter:
    return build_letter(LETTER_PATH) 


def get_updated_cover_letter(original: CoverLetter, **kwargs) -> CoverLetter:
    valid_fields = {f.name for f in fields(CoverLetter)}
    invalid = set(kwargs) - valid_fields
    if invalid:
        raise ValueError(f"Invalid fields: {invalid}. Valid fields: {valid_fields}")
    return replace(original, **kwargs)
