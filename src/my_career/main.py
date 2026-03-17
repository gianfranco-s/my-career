"""Domain logic:
Read JSON files
* resume
* roles
Returns FullResume with subset of WorkExperience
"""
import logging

from config import ROLES_PATH, RESUME_PATH
from domain.resume_loader import build_resume
from domain.convert_to_pdf import export_to_pdf
from domain.filters import filter_work_experiences, get_filters

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    resume = build_resume(RESUME_PATH)

    all_filters = get_filters(ROLES_PATH)

    roles = list(all_filters.keys())
    role = roles[1]

    logger.info(f"Selected {role=}")
    filter = all_filters.get(role)

    filtered_resume = resume
    filtered_resume.work = filter_work_experiences(resume.work, filter)
    output_path = "../../exported.pdf"
    export_to_pdf(resume=resume, output_path=output_path)
    logger.info(f"PDF exported to {output_path=}")
