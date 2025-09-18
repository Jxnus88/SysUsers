import pyfiglet
import sys
import time

import menu.cli as app_cli
import menu.interactive_menu as interac_menu

from utils import clear_screen, launch_pro_cli
from versions_control import get_version
from menu.roles_menu import run_roles_management_menu

from colorama import Fore, Style, init

# Inicializa colorama para que los colores funcionen bien en Windows
init(autoreset=True)

# Obtener versión de la app
try:
    APP_VERSION = get_version()
except Exception:
    APP_VERSION = "Desconocida"

def show_banner():
    banner = pyfiglet.figlet_format("SYS USERS")
    print(f"{Fore.GREEN}{banner}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Versión: {APP_VERSION}{Style.RESET_ALL}\n")

def show_menu():
    print(f"{Fore.CYAN}Seleccione una opción para continuar:{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}1{Style.RESET_ALL}. Usar la aplicación como profesional (línea de comandos)")
    print(f"{Fore.CYAN}2{Style.RESET_ALL}. Gestión de roles predefinidos")
    print(f"{Fore.CYAN}0{Style.RESET_ALL}. Salir\n")
    
                 
def execute_menu_option(opcion):
    clear_screen()
    
    if opcion == '1':
        print(f"{Fore.GREEN}Iniciando modo profesional (CLI)...{Style.RESET_ALL}")
        time.sleep(0.2)
        clear_screen()
        launch_pro_cli(app_cli.main)
        
        
    elif opcion == '2':
        print(f"{Fore.GREEN}Entrando a gestión de roles...{Style.RESET_ALL}")
        time.sleep(0.2)
        clear_screen()
        run_roles_management_menu()
        
    elif opcion == '0':
        print(f"{Fore.CYAN}Saliendo... ¡Hasta luego!{Style.RESET_ALL}")
        time.sleep(0.5)
        clear_screen()
        sys.exit(0)
        
    else:
        print(f"{Fore.RED}Opción inválida, intente de nuevo.{Style.RESET_ALL}")

def main():
    clear_screen()
    show_banner()
    
    while True:
        show_menu()
        
        choice = input(f"{Fore.YELLOW}Ingrese su opción: {Style.RESET_ALL}").strip()
        
        should_exit_menu = execute_menu_option(choice)
        if should_exit_menu:
            break

if __name__ == "__main__":
    main()
