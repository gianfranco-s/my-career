from my_career.domain.models import FullResume, JobDescription, CoverLetter


class PromptHandler:
    def __init__(self, job_description: JobDescription):
        self.jd = job_description.text

    def get_system_prompt(self) -> str:
        return f"You are an experienced Recruiter for the software industry. Tailor the attached resume to the provided job description\n{self.jd}"

    def get_user_prompt(self, content: FullResume | CoverLetter) -> str:
        """Parses content that needs to be adapted to JD"""
        return f"{content}"
