import json
import logging
from pathlib import Path

from domain.models import (ResumeBasics,
                              Location,
                              SocialMediaProfile,
                              Project,
                              PersonalInterest,
                              Education,
                              WorkExperience,
                              Certificate,
                              Language,
                              Skill,
                              FullResume,
                              BaseResumeSection)
                              
logger = logging.getLogger(__name__)

PROJECT_DIR = Path(__file__).parents[3]
RESUME_DIR = PROJECT_DIR / "my-resume"
RESUME_FILENAME = "gianfranco-salomone-cv.json"

RESUME_PATH = RESUME_DIR / RESUME_FILENAME


def _load_resume(resume_path: Path) -> dict:
    with open(resume_path, "r") as f:
        return json.load(f)
    

def _build_basics(basics: dict) -> ResumeBasics:
    location = Location(**basics.get("location"))
    profiles = [SocialMediaProfile(**profile) for profile in basics.get("profiles")]
    parsed_basics = basics
    parsed_basics["location"] = location
    parsed_basics["profiles"] = profiles
    return ResumeBasics(**parsed_basics)


def get_resume_section_definition(raw_section_name: str) -> BaseResumeSection:
    resume_section = {
        "profiles": SocialMediaProfile,
        "work": WorkExperience,
        "education": Education,
        "certificates": Certificate,
        "languages": Language,
        "skills": Skill,
        "projects": Project,
        "interests": PersonalInterest,
    }.get(raw_section_name)

    if resume_section is None:
        logger.warning(f"{raw_section_name=} is not defined")
    
    return resume_section


def build_resume(resume_path: Path) -> FullResume:
    raw_resume = _load_resume(resume_path=resume_path)

    resume = dict()
    resume["basics"] = _build_basics(raw_resume["basics"])

    filtered_resume_keys = [k for k in raw_resume.keys() if k != "basics"]
    for raw_section_name in filtered_resume_keys:
        resume_class = get_resume_section_definition(raw_section_name)
        if resume_class is None:
            continue
        resume[raw_section_name] = [resume_class(**raw_dict) for raw_dict in raw_resume[raw_section_name]]
    
    return FullResume(**resume)
    

if __name__ == "__main__":
    full_resume = build_resume(RESUME_PATH)
    logger.info(full_resume)
