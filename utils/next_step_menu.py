from colorama import Fore, Style


def next_step_menu(option1):
    print(f"\n{Fore.CYAN}¿Qué deseas hacer ahora?{Style.RESET_ALL}\n")
    print(f"  {Fore.YELLOW}1.{Style.RESET_ALL}  {option1}")
    print(f"  {Fore.YELLOW}2.{Style.RESET_ALL}  Volver al menú principal\n")
    
    seleccion = input("Selección: ").strip()
    return seleccion