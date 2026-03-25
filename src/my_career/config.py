from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings
    
PROJECT_ROOT_DIR = Path(__file__).parents[2]


class Settings(BaseSettings):
    source_dir: str = str(PROJECT_ROOT_DIR / "my-resume")
    templates_dir: str = str(PROJECT_ROOT_DIR / "templates")

    resume_filename: str = "resume.json"
    roles_filename: str = "roles.json"
    letter_filename: str = "cover-letter.json"

    resume_template_filename: str = "custom_template.html"
    letter_template_filename: str = "cover_letter_template.html"

    @property
    def source_resume(self) -> Path:
        return Path(self.source_dir) / self.resume_filename

    @property
    def source_roles(self) -> Path:
        return Path(self.source_dir) / self.roles_filename

    @property
    def source_letter(self) -> Path:
        return Path(self.source_dir) / self.letter_filename

    @property
    def template_resume(self) -> Path:
        return Path(self.templates_dir) / self.resume_template_filename

    @property
    def template_letter(self) -> Path:
        return Path(self.templates_dir) / self.letter_template_filename


class AuthSettings(BaseSettings):
    jwt_secret: SecretStr
    jwt_algorithm: str = "HS256"


class OpenAiSettings(BaseSettings):
    openai_api_key: SecretStr


settings = Settings()
openai_settings = OpenAiSettings()
auth_settings = AuthSettings()
