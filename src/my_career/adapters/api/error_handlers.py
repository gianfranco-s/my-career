from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def _error(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}


async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content=_error("VALIDATION_ERROR", str(exc.errors())))


async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content=_error("BAD_REQUEST", str(exc)))


async def unhandled_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=_error("INTERNAL_ERROR", "An unexpected error occurred"))
