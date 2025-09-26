

class HomeError(Exception):
    """Error base para problemas relacionados con el directorio home."""
    pass

class InvalidHomeError(HomeError):
    """El directorio home pertenece a una ruta del sistema no permitida."""
    pass

class PathHomeError(HomeError):
    """La ruta del home no es absoluta o no válida."""
    pass
