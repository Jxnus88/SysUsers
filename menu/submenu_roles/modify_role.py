from colorama import Fore, Style
from utils import clear_screen, get_input, next_step_menu
from services.role_service import RoleService

def modify_role_menu():
    service = RoleService()
    
    while True:
        clear_screen()
        print(f"{Fore.CYAN}=== Modificar rol existente ==={Style.RESET_ALL}\n")
        
        role_name = get_input("Nombre del rol a modificar")
        if not role_name:
            clear_screen()
            break
        
        if not service.role_exists(role_name):
            print(f"{Fore.RED}El rol '{role_name}' no existe.{Style.RESET_ALL}")
            input(f"{Fore.GREEN}Presiona Enter para continuar...{Style.RESET_ALL}")
            continue
        
        current_data = service.get_role_data(role_name)

        print("\nDeja vacío cualquier campo si no deseas modificarlo.\n")

        # Mostrar shell actual
        new_shell = get_input(f"Nuevo shell (actual: {current_data['default_shell']})")

        # Grupos a eliminar primero
        remove_groups_str = get_input("Grupos a ELIMINAR (separados por coma)")

        # Grupos a añadir después
        add_groups_str = get_input("Grupos a AÑADIR (separados por coma)")

        # Procesar listas de grupos
        remove_groups = [g.strip() for g in remove_groups_str.split(",")] if remove_groups_str else None
        add_groups = [g.strip() for g in add_groups_str.split(",")] if add_groups_str else None

        # Mostrar resumen de cambios
        print(f"\nResumen de cambios para el rol '{role_name}':")
        if new_shell:
            print(f"  Nuevo shell: {new_shell}")
        if remove_groups:
            print(f"  Grupos a eliminar: {', '.join(remove_groups)}")
        if add_groups:
            print(f"  Grupos a añadir: {', '.join(add_groups)}")

        confirm = input("\n¿Aplicar estos cambios? (s/N): ").strip().lower()
        if confirm == 's':
            try:
                service.modify_role(
                    role_name=role_name,
                    new_shell=new_shell,
                    add_groups=add_groups,
                    remove_groups=remove_groups
                )
            except Exception as e:
                print(f"{Fore.RED}Error modificando el rol: {e}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}Rol modificado correctamente.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Modificación cancelada.{Style.RESET_ALL}")

        opcion = next_step_menu("Modificar otro rol")
        if opcion == "1":
            continue  # Repite el ciclo para modificar otro rol
        else:
            clear_screen()
            break
