

class UserError(Exception):
    """Excepción base para errores de usuarios."""
    pass

class UserAlreadyExists(UserError):
    """Se lanza cuando el usuario ya existe."""
    pass

class UserCreationError(UserError):
    """Se lanza cuando no se puede crear el usuario."""
    pass

class UserDoNotExists(UserError):
    """Se lanza cuando el usuario no existe."""
    pass