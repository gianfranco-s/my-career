from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from my_career.domain.models import FullResume


def _format_date(date_str: str | None) -> str:
    if not date_str:
        return "Present"
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%b %Y")
    except ValueError:
        return date_str


class ResumeHtmlRenderer:
    """Prepares resume data and renders it to an HTML string using a Jinja2 template."""

    def __init__(self, template_abs_path: str) -> None:
        template_path = Path(template_abs_path)
        if not template_path.exists():
            raise FileNotFoundError(template_abs_path)
        
        self.template_filename = template_path.name
        self.template_dir = template_path.parent

    def render_html_string(self, resume: FullResume) -> str:
        """
        Creates HTML content, based on template
        """
        formatted_resume = self._prepare(resume)
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template(self.template_filename)
        return template.render(cv=formatted_resume)

    def _prepare(self, resume: FullResume) -> dict:
        """
        Converts to dict for Jinja2.
        Adds <DateFormatted> fields and sorts work experience by start date.
        """
        data = asdict(resume)

        for experience in data.get("work", []):
            experience["startDateFormatted"] = _format_date(experience.get("startDate"))
            experience["endDateFormatted"] = _format_date(experience.get("endDate"))

        for education in data.get("education", []):
            education["startDateFormatted"] = _format_date(education.get("startDate"))
            education["endDateFormatted"] = _format_date(education.get("endDate"))

        for project in data.get("projects") or []:
            project["startDateFormatted"] = _format_date(project.get("startDate"))
            project["endDateFormatted"] = _format_date(project.get("endDate"))

        if data.get("work"):
            data["work"] = sorted(data["work"], key=lambda x: x.get("startDate", ""), reverse=True)

        return data


class PdfExporter:
    def __init__(self, template_path: str) -> None:
        self.renderer = ResumeHtmlRenderer(template_path)

    def export(self, resume: FullResume, output_path: str) -> None:
        html_content = self.renderer.render_html_string(resume)
        HTML(string=html_content).write_pdf(output_path)
