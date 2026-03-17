"""Domain logic:
Read JSON files
* resume
* roles
Returns FullResume with subset of WorkExperience
"""
import logging

from my_career.logging_conf import setup_logging

from my_career.config import ROLES_PATH, RESUME_PATH, TEMPLATE_PATH
from my_career.domain.resume_loader import build_resume
from my_career.domain.filters import filter_work_experiences, get_filters
from my_career.adapters.pdf_exporter import PdfExporter

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

    # -------------------------------- Adapters ------------------------------
    output_path = "/home/gsalomone/Documents/02ReposYPracticas/my-career/exported.pdf"
    exporter = PdfExporter(TEMPLATE_PATH)
    exporter.export(filtered_resume, output_path)
    logger.info(f"PDF exported to {output_path=}")
