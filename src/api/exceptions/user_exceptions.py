class UserNotFoundError(Exception):
    """Пользователь не найден"""
    def __init__(self, msg: str):
        super().__init__(msg)


class UserAlreadyExistsError(Exception):
    """Пользователь с таким email уже существует"""
    def __init__(self, msg: str):
        super().__init__(msg)

class PasswordsDoNotMatchError(Exception):
    """Ошибка, если пароли не совпадают"""

    def __init__(self):
        super().__init__("Пароли не совпадают")