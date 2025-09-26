import os

from exceptions import InvalidHomeError, PathHomeError

class HomeValidator:
    
    def __init__(self):
        pass
    
    def validate_home(self, home:str):
        if not home:
            return
        
        if not os.path.isabs(home):
            raise PathHomeError("La ruta del home debe ser absoluta y empeza por '/'.")
        
        if home and any(home.startswith(p) for p in ["/etc", "/bin", "/usr","/lib", "/sbin"]):
            raise InvalidHomeError("¡No uses directorios del sistema como home!")