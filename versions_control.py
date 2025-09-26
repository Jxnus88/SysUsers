
__version__ = "1.0.0"

def get_version() -> str:
    """
    Devuelve la versión actual de la aplicación.
    """
    return __version__

if __name__ == "__main__":
    print(f"SysUsers versión {get_version()}")