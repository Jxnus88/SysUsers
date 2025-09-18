

class InvalidShellError(Exception):
    """Excepción lanzada cuando la shell proporcionada no es válida."""

    def __init__(self, shell_path: str, message: str = None):
        if message is None:
            message = f"La shell '{shell_path}' no existe o no es ejecutable."
        super().__init__(message)
        self.shell_path = shell_path
