from fastapi import status, Request, HTTPException
from src.domain_error import DomainError
from src.input_validate.input_validation_de import InputValidationDE
from src.decode.read_qr_de import ReadQRFailDE

from fastapi.responses import JSONResponse

def error_exception(status_code: int, exc: Exception):
    # RETURN the response object, do not RAISE it
    return JSONResponse(
        status_code=status_code,
        content={
            "error": str(exc),
            "type": exc.__class__.__name__,
        },
    )

def domain_error_handler(request: Request, exc: DomainError):
    if isinstance(exc, ReadQRFailDE):
        return error_exception(status.HTTP_424_FAILED_DEPENDENCY, exc)

    if isinstance(exc, InputValidationDE):
        return error_exception(status.HTTP_424_FAILED_DEPENDENCY, exc)

    return error_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, exc)

def global_error_handler(request: Request, exc: Exception):
    # This catches everything else (KeyError, TypeError, etc.)
    # We return a 500 because these are unexpected system errors
    return error_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, exc)