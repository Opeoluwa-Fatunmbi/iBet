from http import HTTPStatus
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    ValidationError,
    APIException,
)

from apps.core.responses import CustomResponse


class RequestError(APIException):
    default_detail = "An error occured"

    def __init__(self, err_msg: str, status_code: int = 400, data: dict = None) -> None:
        self.status_code = HTTPStatus(status_code)
        self.err_msg = err_msg
        self.data = data

        super().__init__()


def custom_exception_handler(exc, context):
    try:
        response = exception_handler(exc, context)
        if isinstance(exc, AuthenticationFailed):
            exc_list = str(exc).split("DETAIL: ")
            return CustomResponse.error(message=exc_list[-1], status_code=401)
        elif isinstance(exc, RequestError):
            return CustomResponse.error(
                message=exc.err_msg, data=exc.data, status_code=exc.status_code
            )
        elif isinstance(exc, ValidationError):
            errors = exc.detail
            for key in errors:
                errors[key] = str(errors[key][0])
            return CustomResponse.error(
                message="Invalid Entry", data=errors, status_code=422
            )
        else:
            return CustomResponse.error(
                message=exc.detail if hasattr(exc, "detail") else exc,
                status=response.status_code,
            )
    except:
        print(exc)
        return CustomResponse.error(message="Server Error", status_code=500)
