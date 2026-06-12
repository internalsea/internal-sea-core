"""Auth domain errors."""


class AuthError(Exception):
    def __init__(self, message: str, code: str = "auth_error") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class InvalidCredentialsError(AuthError):
    def __init__(self, message: str = "Invalid email or password") -> None:
        super().__init__(message, code="invalid_credentials")


class InactiveUserError(AuthError):
    def __init__(self, message: str = "User account is inactive") -> None:
        super().__init__(message, code="inactive_user")


class UserNotFoundError(AuthError):
    def __init__(self, message: str = "User not found") -> None:
        super().__init__(message, code="user_not_found")


class DuplicateUserEmailError(AuthError):
    def __init__(self, message: str = "A user with this email already exists") -> None:
        super().__init__(message, code="duplicate_user_email")


class InsufficientPermissionsError(AuthError):
    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message, code="insufficient_permissions")
