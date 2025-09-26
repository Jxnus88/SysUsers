from pyfiglet import Figlet
from colorama import Fore, Style

from versions_control import get_version

try:
    APP_VERSION = get_version()
except Exception:
    APP_VERSION = "Desconocida"

def show_welcome():
    banner = Figlet(font='slant')
    print(f"{Fore.GREEN}{banner.renderText('SysUsers')}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Versión: {APP_VERSION}{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}Bienvenido a SysUsers - Administrador de usuarios Linux (CLI){Style.RESET_ALL}\n")
    print(f"\nEscribe 'manual' para obtener información del sistema.\n")