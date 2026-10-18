import math

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


def _sanitize_for_json(val):
    if isinstance(val, (Exception, type)):
        return str(val)
    if isinstance(val, dict):
        return {k: _sanitize_for_json(v) for k, v in val.items()}
    if isinstance(val, (list, tuple)):
        return [_sanitize_for_json(v) for v in val]
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return str(val)
    if isinstance(val, str):
        return val.encode("utf-8", "replace").decode("utf-8")
    return val


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(IntegrityError)
    def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Database integrity conflict occurred."},
        )

    @app.exception_handler(OverflowError)
    def overflow_error_handler(request: Request, exc: OverflowError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Numeric value is out of acceptable range."},
        )

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": _sanitize_for_json(exc.errors())},
        )
