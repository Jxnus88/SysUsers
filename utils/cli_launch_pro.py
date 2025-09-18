import shlex
import menu.cli as app_cli
import time

from colorama import Fore, Style
from utils import clear_screen
from .cli_clear_screen import clear_screen_cli

def launch_pro_cli(main_func):
    app_cli.show_welcome()
    print(f"{Fore.GREEN}Entrando a CLI profesional. Escribe 'exit' para salir del sistema.{Style.RESET_ALL}\n")

    while True:
        try:
            command = input("sysusers > ").strip()
            
            if not command:
                continue
            
            command_lower = command.lower()

            if command_lower in ["exit", "salir", "quit", "q"]:
                print(f"{Fore.CYAN}Saliendo de CLI profesional...{Style.RESET_ALL}")
                time.sleep(0.5)
                clear_screen()
                break
            
            if command_lower == "banner":
                clear_screen()
                app_cli.show_welcome()
                continue
            
            if command_lower in ['cls', 'clear']:
                clear_screen_cli()
                continue
            
            if command_lower == "manual":
                clear_screen()
                app_cli.show_manual()
                continue
            
            args = shlex.split(command)
            main_func(args)
            
        except Exception as e:
            if "Fin del comando" in str(e):
                continue
            
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

