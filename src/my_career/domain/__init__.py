from pathlib import Path

RESUME_FILENAME = "gianfranco-salomone-cv.json"
ROLES_FILENAME = "gianfranco-salomone-roles.json"

PROJECT_ROOT_DIR = Path(__file__).parents[3]
RESUME_DIR = PROJECT_ROOT_DIR / "my-resume"

RESUME_PATH = RESUME_DIR / RESUME_FILENAME
ROLES_PATH = RESUME_DIR / ROLES_FILENAME
