import shlex, argparse

from colorama import Fore, Style
from .show_manual import show_manual
from .show_welcome import show_welcome
from ..argparser_config import parse_args
from utilis import (
    clear_screen, 
    clear_screen_cli
    )

def launch_pro_cli(main_func):

    show_welcome()
    print(f"{Fore.GREEN}Entrando a CLI profesional. Escribe 'exit' para salir del sistema.{Style.RESET_ALL}\n")
    
    while True:
        try:
            command = input("sysusers > ").strip()
            
            if not command:
                continue
            
            command_lower = command.lower()
            
            if command_lower in ["exit", "quit", "salir", "q"]:
                clear_screen()
                break
            
            if command_lower == "banner":
                clear_screen()
                show_welcome()
                continue
            
            if command_lower in ['cls', 'clear']:
                clear_screen_cli()
                continue
            
            if command_lower == "manual":
                clear_screen()
                show_manual()
                continue
            
            args_list = shlex.split(command)
            args = parse_args(args_list)

            try:
                main_func(args)
            except argparse.ArgumentError as ae:
                print(f"{Fore.RED}[!] Error de argumentos: {ae}{Style.RESET_ALL}")
            except SystemExit:
                print(f"{Fore.RED}[!] Argumentos inválidos. Usa '-h' para ayuda.{Style.RESET_ALL}")
            except Exception as e:
                if str(e) == "HelpShown":
                    pass
                elif str(e) == "ArgumentError":
                    print(f"{Fore.RED}[!] Argumentos inválidos. Usa '-h' para ayuda.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[X] Error inesperado (func): {e}{Style.RESET_ALL}")
                    
        except Exception as e:
            if str(e) == "HelpShown":
                pass
            elif str(e) == "ArgumentError":
                print(f"{Fore.RED}[!] Argumentos inválidos. Usa '-h' para ayuda.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[X] Error inesperado (parser): {e}{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}[*] CLI interrumpido. Saliendo...{Style.RESET_ALL}")
            clear_screen()