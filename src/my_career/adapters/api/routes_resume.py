from fastapi import APIRouter, Request

from my_career.ports.resume_boundary import ResumeBoundary

router = APIRouter()

 
@router.get("/resume")
def get_resume(request: Request):
    service: ResumeBoundary = request.app.state.resume_service
    return service.get_resume()


@router.get("/resume/roles")
def get_resume_roles(request: Request):
    service: ResumeBoundary = request.app.state.resume_service
    return service.get_available_roles()


@router.get("/resume/filters-for-role")
def get_resume_filters_for_role(request: Request, role: str):
    service: ResumeBoundary = request.app.state.resume_service
    return service.get_filters_for_role(role)


@router.get("/resume/filtered")
def get_filtered_resume(request: Request, role: str):
    service: ResumeBoundary = request.app.state.resume_service
    return service.get_filtered_resume(role)
