# menu/add_role.py
from colorama import Fore, Style
from services import RoleService
from utils import clear_screen, get_input, next_step_menu

def add_role_menu():
    clear_screen()
    print(f"{Fore.CYAN}=== Crear nuevo rol ==={Style.RESET_ALL}\n")
    service = RoleService()

    while True:
        role_name = get_input("Nombre del nuevo rol")
        if not role_name:
            return
        if service.role_exists(role_name):
            print(f"{Fore.RED}✗ El rol '{role_name}' ya existe.{Style.RESET_ALL}")
            continue
        break

    default_shell = get_input("Shell por defecto (por defecto: /bin/bash)") or "/bin/bash"
    raw_groups = get_input("Grupos separados por coma (ej: sudo,admin)")
    if raw_groups is None:
        return
    groups = [g.strip() for g in raw_groups.split(",") if g.strip()] if raw_groups else []

    # Mostrar resumen para confirmación
    print(f"\n{Fore.BLUE}Revisión del nuevo rol:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Nombre:{Style.RESET_ALL} {role_name}")
    print(f"  {Fore.YELLOW}Shell por defecto:{Style.RESET_ALL} {default_shell}")
    print(f"  {Fore.YELLOW}Grupos:{Style.RESET_ALL} {', '.join(groups) if groups else 'Ninguno'}")

    confirmar = input(f"\n{Fore.CYAN}¿Deseas guardar este rol? (s/N): {Style.RESET_ALL}").strip().lower()
    if confirmar != 's':
        print(f"{Fore.CYAN}[*] Rol cancelado. No se realizaron cambios.{Style.RESET_ALL}")
        input("Presiona Enter para continuar...")
        clear_screen()
        return

    try:
        service.create_role(role_name, default_shell, groups)
        print(f"{Fore.GREEN}✓ Rol '{role_name}' creado exitosamente.{Style.RESET_ALL}")
    except ValueError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    opcion = next_step_menu("Crear otro rol")
    if opcion == "1":
        clear_screen()
        add_role_menu()
    else:
        clear_screen()
