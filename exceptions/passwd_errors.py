

class PasswdError(Exception):
    """ Excepción base para errores relacionados con contraseñas."""
    pass

class NotPasswdError(PasswdError):
    """Se lanza cuando no se proporciona una contraseña."""
    pass