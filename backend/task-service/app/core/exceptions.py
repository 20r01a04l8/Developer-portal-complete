class BaseAPIException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(BaseAPIException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ConflictException(BaseAPIException):
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, status_code=409)


class ValidationException(BaseAPIException):
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=422)


class UnauthorizedException(BaseAPIException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenException(BaseAPIException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)
