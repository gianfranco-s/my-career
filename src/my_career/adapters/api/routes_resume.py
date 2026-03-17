from fastapi import APIRouter, Request

from my_career.use_cases.resume import get_predefined_roles, get_resume_filters, get_resume_with_filtered_work_exp

router = APIRouter()


@router.get("/resume")
def get_resume(request: Request):
    return request.app.state.resume


@router.get("/resume/roles")
def get_resume_roles(request: Request):
    return get_predefined_roles()


@router.get("/resume/filters-for-role")
def get_resume_filters_for_role(request: Request, role: str):
    return get_resume_filters(request.app.state.resume, role)


@router.get("/resume/filtered")
def get_filtered_resume(request: Request, role: str):
    return get_resume_with_filtered_work_exp(resume=request.app.state.resume, role=role)
