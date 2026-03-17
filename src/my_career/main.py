"""Domain logic:
Read JSON files
* resume
* roles
Returns FullResume with subset of WorkExperience
"""
import logging

from my_career.logging_conf import setup_logging

from my_career.config import ROLES_PATH, RESUME_PATH, RESUME_TEMPLATE_PATH, LETTER_TEMPLATE_PATH, LETTER_PATH
from my_career.domain.resume_loader import build_resume
from my_career.domain.letter_loader import build_letter
from my_career.domain.filters import filter_work_experiences, get_filters
from my_career.adapters.pdf_exporter import ResumePdfExporter, LetterPdfExporter

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    setup_logging()

    # -------------------------------- Domain --------------------------------
    resume = build_resume(RESUME_PATH)

    all_filters = get_filters(ROLES_PATH)

    roles = list(all_filters.keys())
    role = roles[1]

    logger.info(f"Selected {role=}")
    filter = all_filters.get(role)

    filtered_resume = filter_work_experiences(resume, filter)

    cover_letter = build_letter(LETTER_PATH)

    # -------------------------------- Adapters ------------------------------
    # We can mock this to begin with
    # Set up Adapter
    # Call upstream llm (original_resume, JD) -> AIAdaptedResume
    # Call upstream llm (adapted_resume, JD) -> AICoverLetter (needs template)

    output_path = "/home/gsalomone/Documents/02ReposYPracticas/my-career/exported_resume.pdf"
    exporter = ResumePdfExporter(RESUME_TEMPLATE_PATH)
    exporter.export(filtered_resume, output_path)
    logger.info(f"PDF resume exported to {output_path=}")

    output_path = "/home/gsalomone/Documents/02ReposYPracticas/my-career/exported_cover_letter.pdf"
    exporter = LetterPdfExporter(LETTER_TEMPLATE_PATH)
    exporter.export(cover_letter, output_path)
    logger.info(f"PDF cover letter exported to {output_path=}")
