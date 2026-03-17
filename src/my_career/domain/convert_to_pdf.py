from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from my_career.domain.models import FullResume


TEMPLATES_DIR = Path(__file__).parents[3] / "templates"


def _format_date(date_str: str | None) -> str:
    if not date_str:
        return "Present"
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%b %Y")
    except ValueError:
        return date_str


def _prepare_resume_data(resume: FullResume) -> dict:
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


def _render_html(resume_data: dict, template_filename: str = "custom_template.html") -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template(template_filename)
    return template.render(cv=resume_data)


def export_to_pdf(resume: FullResume, output_path: str) -> None:
    resume_data = _prepare_resume_data(resume)
    # html_content = _render_html(resume_data, "custom_template.html")
    # html_content = _render_html(resume_data, "harvard_template.html")
    html_content = _render_html(resume_data, "harvard_template_v2.html")
    HTML(string=html_content).write_pdf(output_path)

