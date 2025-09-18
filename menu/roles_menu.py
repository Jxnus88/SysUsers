from colorama import Fore, Style

from utils import clear_screen
from managers import RoleManager
from menu.submenu_roles import add_role_menu, modify_role_menu

def run_roles_management_menu():
    while True:
        print(f"\n{Fore.CYAN}=== Gestión de Roles ==={Style.RESET_ALL}\n")
        print(f"  {Fore.YELLOW}1.{Style.RESET_ALL} Añadir nuevo rol predefinido (En desarrollo)")
        print(f"  {Fore.YELLOW}2.{Style.RESET_ALL} Modificar rol existente (En desarrollo)")
        print(f"  {Fore.YELLOW}3.{Style.RESET_ALL} Ver lista de roles")
        print(f"  {Fore.YELLOW}0.{Style.RESET_ALL} Volver al menú principal\n")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == '1':
            clear_screen()
            add_role_menu()

        elif opcion == '2':
            clear_screen()
            modify_role_menu()

        elif opcion == '3':
            clear_screen()
            rm = RoleManager()
            print(f"{Fore.CYAN}=== Lista de roles ==={Style.RESET_ALL}\n")
            for role in rm.list_roles():
                data = rm.get_role_data(role)
                print(f"{Fore.YELLOW}- {role}{Style.RESET_ALL}: Shell: {data['default_shell']}, Grupos: {', '.join(data['groups']) or 'Ninguno'}")
            input(f"\n{Fore.GREEN}Presiona Enter para volver...{Style.RESET_ALL}")
            clear_screen()

        elif opcion == '0':
            clear_screen()
            break

        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}")
