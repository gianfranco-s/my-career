from domain.resume_loader import build_resume
from domain.convert_to_pdf import export_to_pdf
from domain.filters import filter_work_experiences, get_filters


resume = build_resume()

all_filters = get_filters("/home/gsalomone/Documents/02ReposYPracticas/my-career/my-resume/gianfranco-salomone-roles.json")
roles = list(all_filters.keys())

role = roles[1]

print(f"Selected {role=}")
filter = all_filters.get(role)

filtered_resume = resume
filtered_resume.work = filter_work_experiences(resume.work, filter)
output_path = "../../exported.pdf"
export_to_pdf(resume=resume, output_path=output_path)
print(f"PDF exported to {output_path=}")
