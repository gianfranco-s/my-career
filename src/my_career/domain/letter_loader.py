"""
Loads a resume from a JSON file and maps it to domain models.

Kept in domain because the resume will always be sourced from a local JSON file —
there is no alternative implementation to swap in, so a port abstraction adds no value.
"""
import json
import logging
from pathlib import Path
from datetime import datetime

from my_career.domain.models import CoverLetter

logger = logging.getLogger(__name__)


def _load_letter(letter_path: Path) -> dict:
    with open(letter_path, "r") as f:
        return json.load(f)


def build_letter(letter_path: Path) -> CoverLetter:
    raw_data = _load_letter(letter_path)
    raw_data["date"] = datetime.today().strftime("%B %d, %Y")

    return CoverLetter(**raw_data)
