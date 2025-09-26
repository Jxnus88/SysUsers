import os
from exceptions import InvalidShellError


class ShellValidator:
    
    def __init__(self):
        pass
    
    def validate_shell(self, shell:str):
        
        if not shell:
            return
        
        if not os.path.isfile(shell) or not os.access(shell, os.X_OK):
            raise InvalidShellError(f"Shell '{shell}' no válida.")