"""Domain logic:
Read JSON files
* resume
* roles
Returns FullResume with subset of WorkExperience
"""
import logging

from my_career.logging_conf import setup_logging
setup_logging()

from my_career.config import ROLES_PATH, RESUME_PATH
from my_career.domain.resume_loader import build_resume
from my_career.domain.convert_to_pdf import export_to_pdf
from my_career.domain.filters import filter_work_experiences, get_filters

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # -------------------------------- Domain --------------------------------
    resume = build_resume(RESUME_PATH)

    all_filters = get_filters(ROLES_PATH)

    roles = list(all_filters.keys())
    role = roles[1]

    logger.info(f"Selected {role=}")
    filter = all_filters.get(role)

    filtered_resume = filter_work_experiences(resume, filter)

    # -------------------------------- Adapters ------------------------------
    output_path = "../../exported.pdf"
    export_to_pdf(resume=resume, output_path=output_path)
    logger.info(f"PDF exported to {output_path=}")
