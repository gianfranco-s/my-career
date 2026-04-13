from openai import OpenAI

from my_career.domain.models import CoverLetter, JobDescription
from my_career.domain.prompt_handler import PromptHandler
from my_career.adapters.openai_tailor import OpenAiTailor
from my_career.use_cases.cover_letter import CoverLetterService


class AiCoverLetterService:
    def __init__(self, cover_letter_service: CoverLetterService, openai_client: OpenAI):
        self.__service = cover_letter_service
        self.__client = openai_client

    def tailor_cover_letter(self, job_description: JobDescription) -> CoverLetter:
        letter = self.__service.get_cover_letter()
        tailor = OpenAiTailor(self.__client, PromptHandler(job_description))
        return tailor.get_tailored_letter(letter)

    def tailor_cover_letter_pdf(self, job_description: JobDescription) -> bytes:
        tailored = self.tailor_cover_letter(job_description)
        return self.__service.export_letter_pdf(tailored)
