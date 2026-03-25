"""Domain logic:
Read JSON files
* resume
* roles
Returns FullResume with subset of WorkExperience
"""
import logging

from my_career.logging_conf import setup_logging
from my_career.config import settings, openai_settings
from my_career.domain.filters import filter_work_experiences, get_filters
from my_career.domain.letter_loader import build_letter
from my_career.domain.models import JobDescription
from my_career.domain.prompt_handler import PromptHandler
from my_career.domain.resume_loader import build_resume
from my_career.adapters.pdf_exporter import ResumePdfExporter, LetterPdfExporter
from my_career.adapters.openai_tailor import OpenAiTailor

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    ADAPT_USING_JD: bool = False

    setup_logging()

    # -------------------------------- Domain --------------------------------
    resume = build_resume(settings.source_resume)

    all_filters = get_filters(settings.source_roles)

    roles = list(all_filters.keys())
    role = roles[1]

    logger.debug(f"Selected {role=}")
    filter = all_filters.get(role)

    filtered_resume = filter_work_experiences(resume, filter)

    cover_letter = build_letter(settings.source_letter)

    job_description = JobDescription(text="This is a test JD. Change the tone to be that of a pirate")
    prompt_handler = PromptHandler(job_description=job_description)
    logger.debug(prompt_handler.get_system_prompt())

    # -------------------------------- Adapters ------------------------------
    
    final_resume = filtered_resume
    final_letter = cover_letter

    if ADAPT_USING_JD:
        from openai import OpenAI
        client = OpenAI(api_key=openai_settings.openai_api_key)
        tailor = OpenAiTailor(client=client, prompt_handler=prompt_handler)
        tailored_letter = tailor.get_tailored_letter(content=cover_letter)
        logger.debug(tailored_letter)
        
        tailored_resume = tailor.get_tailored_resume(content=filtered_resume)
        logger.debug(tailored_resume)

        final_resume = tailored_resume
        final_letter = tailored_letter

    output_path = "/home/gsalomone/Documents/02ReposYPracticas/my-career/exported_resume.pdf"
    exporter = ResumePdfExporter(settings.template_resume)
    exporter.export(final_resume, output_path)
    logger.info(f"PDF resume exported to {output_path=}")

    output_path = "/home/gsalomone/Documents/02ReposYPracticas/my-career/exported_cover_letter.pdf"
    exporter = LetterPdfExporter(settings.template_letter)
    exporter.export(final_letter, output_path)
    logger.info(f"PDF cover letter exported to {output_path=}")
