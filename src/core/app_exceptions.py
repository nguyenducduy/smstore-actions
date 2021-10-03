from fastapi import Request
from starlette.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, message: str):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - message={self.message}> -"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "message": exc.message,
        },
    )


class AppException(object):
    class EventTriggerFail(AppExceptionCase):
        def __init__(self, message: str = None):
            status_code = 400
            message = message
            AppExceptionCase.__init__(self, status_code, message)

    class SendActivateCodeFail(AppExceptionCase):
        def __init__(self, message: str = None):
            status_code = 400
            message = 'Không thể gửi mã kích hoạt'
            AppExceptionCase.__init__(self, status_code, message)

    class RegisterUserFail(AppExceptionCase):
        def __init__(self, message: str = None):
            status_code = 400
            message = message
            AppExceptionCase.__init__(self, status_code, message)
    
    class ActivateUserFail(AppExceptionCase):
        def __init__(self, message: str = None):
            status_code = 400
            message = message
            AppExceptionCase.__init__(self, status_code, message)

    class LoginUserFail(AppExceptionCase):
        def __init__(self, message: str = None):
            status_code = 400
            message = message
            AppExceptionCase.__init__(self, status_code, message)

    class InvalidCart(AppExceptionCase):
        def __init__(self, message: str = None):
            status_code = 400
            message = 'Invalid Cart!!!'
            AppExceptionCase.__init__(self, status_code, message)
    
    class CreateOrderFail(AppExceptionCase):
        def __init__(self, message: str = None):
            status_code = 400
            message = 'Không thể đặt hàng, vui lòng thử lại sau.'
            AppExceptionCase.__init__(self, status_code, message)

    