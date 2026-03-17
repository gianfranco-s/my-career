import os
from pathlib import Path


PROJECT_ROOT_DIR = Path(__file__).parents[2]

DEFAULT_RESUME_DIR = PROJECT_ROOT_DIR / "my-resume"

RESUME_DIR: str = os.environ.get("RESUME_DIR", DEFAULT_RESUME_DIR)
RESUME_FILENAME: str = os.environ.get("RESUME_FILENAME", "resume.json")
ROLES_FILENAME: str = os.environ.get("ROLES_FILENAME", "roles.json")


RESUME_PATH = RESUME_DIR / RESUME_FILENAME
ROLES_PATH = RESUME_DIR / ROLES_FILENAME
