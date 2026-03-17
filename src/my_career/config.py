import os
from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parents[2]

DEFAULT_RESUME_DIR = PROJECT_ROOT_DIR / "my-resume"
DEFAULT_TEMPLATES_DIR = PROJECT_ROOT_DIR / "templates"

RESUME_DIR: str = os.environ.get("RESUME_DIR", DEFAULT_RESUME_DIR)
TEMPLATES_DIR: str = os.environ.get("TEMPLATES_DIR", DEFAULT_TEMPLATES_DIR)

RESUME_FILENAME: str = os.environ.get("RESUME_FILENAME", "resume.json")
ROLES_FILENAME: str = os.environ.get("ROLES_FILENAME", "roles.json")
TEMPLATE_FILENAME: str = os.environ.get("TEMPLATE_FILENAME", "custom_template.html")


RESUME_PATH = RESUME_DIR / RESUME_FILENAME
ROLES_PATH = RESUME_DIR / ROLES_FILENAME
TEMPLATE_PATH = TEMPLATES_DIR / TEMPLATE_FILENAME
