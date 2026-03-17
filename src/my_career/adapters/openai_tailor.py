from dataclasses import replace
from typing import Any

from openai import OpenAI
from pydantic import create_model

from my_career.domain.models import CoverLetter, FullResume, WorkExperience, Location
from my_career.domain.prompt_handler import PromptHandler
from my_career.adapters.pydantic_utils import dataclass_to_basemodel

CoverLetterSchema = dataclass_to_basemodel(CoverLetter)
WorkExperienceSchema = dataclass_to_basemodel(WorkExperience)
TailoredResumeSchema = create_model("TailoredResumeSchema", work=(list[WorkExperienceSchema], ...))


def _to_work_experience(data: dict) -> WorkExperience:
    data["location"] = Location(**data["location"])
    return WorkExperience(**data)


class OpenAiTailor:
    def __init__(self, client: OpenAI, prompt_handler: PromptHandler):
        self.__client = client
        self.__prompt_handler = prompt_handler

    def get_tailored_letter(self, content: CoverLetter, dry_run: bool = False) -> CoverLetter | None:
        user_content = self.__prompt_handler.get_user_prompt(content)

        if dry_run:
            return None

        res = self.__call_upstream(user_content=user_content, text_format=CoverLetterSchema)
        parsed = res.output_parsed
        return CoverLetter(**parsed.model_dump())


    def get_tailored_resume(self, content: FullResume, dry_run: bool = False) -> FullResume | None:
        if dry_run:
            return None

        user_content = self.__prompt_handler.get_user_prompt(content)
        res = self.__call_upstream(user_content=user_content, text_format=TailoredResumeSchema)
        tailored_work = [_to_work_experience(we.model_dump()) for we in res.output_parsed.work]
        return replace(content, work=tailored_work)


    def __call_upstream(self, user_content: str, text_format: Any) -> Any:
        system_input = {
            "role": "system",
            "content": self.__prompt_handler.get_system_prompt()
        }
        user_input = {
            "role": "user",
            "content": user_content
        }

        payload = dict(
            model="gpt-4o-2024-08-06",
            input=[system_input, user_input],
            text_format=text_format
        )
        
        return self.__client.responses.parse(**payload)
