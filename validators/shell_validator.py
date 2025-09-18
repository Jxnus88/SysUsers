import os
from exceptions.shell_errors import InvalidShellError

class ShellValidator:
    @staticmethod
    def validate(shell_path: str) -> None:
        """
        Valida que la shell existe y es ejecutable.
        Lanza InvalidShellError si no es válida.
        """
        if not shell_path:
            # Permitimos que no se pase shell, se usa por defecto
            return
        
        if not os.path.isfile(shell_path) or not os.access(shell_path, os.X_OK):
            raise InvalidShellError(shell_path)
