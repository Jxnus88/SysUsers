from colorama import Fore, Style, init
from services.role_service import RoleService

init(autoreset=True)

role_service = RoleService()

def handle_show_role(args):
    role_name = args.role_name
    
    if not role_service.role_exists(role_name):
        print(f"{Fore.RED}[X] El rol '{role_name}' no existe.{Style.RESET_ALL}")
        return
    
    data = role_service.get_role_data(role_name)
    
    shell = data.get("default_shell")
    shell_display = shell if shell else "No asignado"
    
    groups = data.get("groups", [])
    groups_display = ", ".join(groups) if groups else "No asignado"
    
    print(f"{Fore.CYAN}Detalles del rol '{role_name}':{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Shell por defecto: {shell_display}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Grupos:           {groups_display}{Style.RESET_ALL}")

def handle_list_roles(args=None, role_service=None):
    roles = role_service.list_roles()
    if not roles:
        print(f"{Fore.YELLOW}[!] No hay roles definidos.{Style.RESET_ALL}")
        return
    print(f"{Fore.CYAN}Roles disponibles:{Style.RESET_ALL}")
    for role in roles:
        print(f" - {role}")

def handle_create_role(args):
    try:
        role_service.create_role(
            role_name=args.role_name,
            shell=args.shell or "/bin/bash",
            groups=args.groups or []
        )
        print(f"{Fore.GREEN}[✓] Rol '{args.role_name}' creado correctamente.{Style.RESET_ALL}")
    except ValueError as e:
        print(f"{Fore.RED}[X] Error: {e}{Style.RESET_ALL}")

def handle_modify_role(args):
    try:
        role_service.modify_role(
            role_name=args.role_name,
            new_shell=args.shell,
            add_groups=args.add_groups,
            remove_groups=args.remove_groups,
            replace_groups=args.replace_groups
        )
        print(f"{Fore.GREEN}[✓] Rol '{args.role_name}' modificado correctamente.{Style.RESET_ALL}")
    except ValueError as e:
        print(f"{Fore.RED}[X] Error: {e}{Style.RESET_ALL}")

def handle_delete_role(args):
    try:
        role_service.delete_role(args.role_name)
        print(f"{Fore.GREEN}[✓] Rol '{args.role_name}' eliminado correctamente.{Style.RESET_ALL}")
    except ValueError as e:
        print(f"{Fore.RED}[X] Error: {e}{Style.RESET_ALL}")
