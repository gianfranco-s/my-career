from fastapi import APIRouter, Request, Response

from my_career.ports.resume_boundary import ResumeBoundary

router = APIRouter(tags=["resume"])


@router.get("")
def get_resume(request: Request):
    service: ResumeBoundary = request.app.state.resume_service
    return service.get_resume()


@router.get("/roles")
def get_resume_roles(request: Request):
    service: ResumeBoundary = request.app.state.resume_service
    return service.get_available_roles()


@router.get("/filters-for-role")
def get_resume_filters_for_role(request: Request, role: str):
    service: ResumeBoundary = request.app.state.resume_service
    return service.get_filters_for_role(role)


@router.get("/filtered")
def get_filtered_resume(request: Request, role: str):
    service: ResumeBoundary = request.app.state.resume_service
    return service.get_filtered_resume(role)


@router.get("/pdf")
def get_resume_pdf(request: Request, role: str | None = None):
    """Returns pdf at <api-root>/resume/pdf"""
    service: ResumeBoundary = request.app.state.resume_service
    pdf_bytes = service.export_pdf(role)
    return Response(content=pdf_bytes, media_type="application/pdf")
