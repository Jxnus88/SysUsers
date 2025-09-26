import os, sys

def clear_screen():
    if sys.platform == "win32":
        os.system('cls')
    else:
        os.system('clear')
        
        
def clear_screen_cli():
    """Limpia la pantalla según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')