from fastapi import HTTPException
from starlette import status

class ForbiddenError(HTTPException):
    """Недостаточно прав для доступа к ресурсу"""
    def __init__(self, detail: str = "Недостаточно прав для доступа к ресурсу"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
