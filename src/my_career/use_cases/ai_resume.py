from openai import OpenAI

from my_career.domain.models import FullResume, JobDescription
from my_career.domain.prompt_handler import PromptHandler
from my_career.adapters.openai_tailor import OpenAiTailor
from my_career.use_cases.resume import ResumeService


class AiResumeService:
    def __init__(self, resume_service: ResumeService, openai_client: OpenAI):
        self.__service = resume_service
        self.__client = openai_client

    def tailor_resume(self, job_description: JobDescription, role: str | None = None) -> FullResume:
        resume = self.__service.get_filtered_resume(role) if role else self.__service.get_resume()
        tailor = OpenAiTailor(self.__client, PromptHandler(job_description))
        return tailor.get_tailored_resume(resume)

    def tailor_resume_pdf(self, job_description: JobDescription, role: str | None = None) -> bytes:
        tailored = self.tailor_resume(job_description, role)
        return self.__service.export_resume_pdf(tailored)
