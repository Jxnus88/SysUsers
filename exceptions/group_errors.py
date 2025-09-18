

class MissingGroupError(Exception):
    """Excepción lanzada cuando el grupo no existe."""

    def __init__(self, group_name: str, message: str = None):
        if message is None:
            message = f"El grupo '{group_name}' no existe."
        super().__init__(message)
        self.group_name = group_name
