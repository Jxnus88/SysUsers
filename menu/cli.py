from colorama import Fore, Style
from pyfiglet import Figlet
from versions_control import get_version

from services.user_service import UserService
from services.role_service import RoleService
from handlers import user_handler, csv_handler, role_handler
from managers import UserManager
from utils import ArgumentParserNoExit, launch_pro_cli

try:
    APP_VERSION = get_version()
except Exception:
    APP_VERSION = "Desconocida"


def parse_args(argv=None):
    parser = ArgumentParserNoExit(
    description="SysUsers - Administrador de usuarios para Linux"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Comandos disponibles"
    )

    # Subcomando: create
    create_parser = subparsers.add_parser(
        "create",
        help="Crear un nuevo usuario en el sistema."
    )
    create_parser.add_argument(
        "username",
        help="Nombre del usuario a crear."
    )
    create_parser.add_argument(
        "--shell",
        help="Shell del usuario (se ignora si usas --role). Ejemplo: /bin/bash",
        default="/bin/bash"
    )
    create_parser.add_argument(
        "--home",
        help="Directorio home del usuario. Si no se especifica, se asigna el default."
    )
    grouping = create_parser.add_mutually_exclusive_group()
    grouping.add_argument(
        "--groups",
        help=(
            "Lista de grupos secundarios separados por comas. "
            "No se puede usar junto con --role. Ejemplo: 'staff,developers'"
        )
    )
    grouping.add_argument(
        "--role",
        help=(
            "Rol predefinido que asigna automáticamente grupos y shell según data/roles.json. "
            "No se puede usar junto con --groups. Ejemplo: 'developer'"
        )
    )
    create_parser.add_argument(
        "--temp-pass",
        required=True,
        help=(
            "Contraseña temporal para el usuario (se pedirá cambiarla en el primer inicio de sesión)."
        )
    )

    # Subcomando: delete
    delete_parser = subparsers.add_parser(
        "delete",
        help="Eliminar un usuario del sistema."
    )
    delete_parser.add_argument(
        "username",
        help="Nombre del usuario a eliminar."
    )

    # Subcomando: list-users
    subparsers.add_parser(
        "list-users",
        help="Listar todos los usuarios normales del sistema (UID >= 1000)."
    )

    # Subcomando: search-user-id
    list_user_parser = subparsers.add_parser(
        "search-user-id",
        help="Buscar un usuario por su UID."
    )
    list_user_parser.add_argument(
        "uid",
        type=int,
        help="UID del usuario a consultar."
    )

    # Subcomando: import
    import_parser = subparsers.add_parser(
        "import",
        help="Importar usuarios desde un archivo CSV."
    )
    import_parser.add_argument(
        "csvfile",
        help="Ruta al archivo CSV con los datos de los usuarios."
    )
    
    # Subcomando: list-roles
    subparsers.add_parser(
        "list-roles",
        help="Listar los roles disponibles definidos en data/roles.json."
    )
    
    return parser.parse_args(argv)


def show_welcome():
    banner = Figlet(font='slant')
    print(f"{Fore.GREEN}{banner.renderText('SysUsers')}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Versión: {APP_VERSION}{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}Bienvenido a SysUsers - Administrador de usuarios Linux (CLI){Style.RESET_ALL}\n")
    print(f"\nEscribe 'manual' para obtener información del sistema.\n")

    
def show_manual():
    """Muestro toda la información detallada del CLI."""
    print(f"\n{Fore.WHITE}Modo Profesional (CLI interactiva):{Style.RESET_ALL}")
    print(f"  En este modo puedes escribir directamente los comandos sin 'sysusers.cli' delante.")
    print(f"  Ejemplo de comandos que puedes escribir:")
    print(f"    {Fore.YELLOW}list-users{Style.RESET_ALL}")
    print(f"    {Fore.YELLOW}create pedro --shell /bin/bash --groups staff,users --temp-pass Pedro123{Style.RESET_ALL}")
    print(f"    {Fore.YELLOW}delete pedro{Style.RESET_ALL}")
    print(f"    {Fore.YELLOW}search-user-id 1001{Style.RESET_ALL}")
    print(f"    {Fore.YELLOW}import usuarios.csv{Style.RESET_ALL}")
    print(f"    {Fore.YELLOW}list-roles{Style.RESET_ALL}")
    print(f"\n  Escribe 'exit' o 'quit' para salir del modo CLI profesional.\n")

    print(f"{Fore.WHITE}Uso básico para crear usuario (línea de comandos estándar):{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}create pedro --shell /bin/bash --home /home/pedro --groups staff,users --temp-pass Pedro123{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}create ana --role developer --temp-pass Ana1234{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Otros comandos disponibles (modo estándar):{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}create{Style.RESET_ALL}            - Crear un usuario")
    print(f"  {Fore.CYAN}delete{Style.RESET_ALL}            - Eliminar un usuario")
    print(f"  {Fore.CYAN}list-users{Style.RESET_ALL}        - Listar todos los usuarios")
    print(f"  {Fore.CYAN}search-user-id{Style.RESET_ALL}    - Buscar usuario por UID")
    print(f"  {Fore.CYAN}import{Style.RESET_ALL}            - Importar usuarios desde CSV")
    print(f"  {Fore.CYAN}list-roles{Style.RESET_ALL}        - Mostrar roles disponibles")
    
    print(f"\n{Fore.WHITE}Ejemplos de ayuda con comandos:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}create -h{Style.RESET_ALL}         Muestra ayuda para crear usuarios")
    print(f"  {Fore.YELLOW}delete -h{Style.RESET_ALL}         Muestra ayuda para eliminar usuarios")
    print(f"\nPara más opciones usa: {Fore.YELLOW}-h{Style.RESET_ALL} o {Fore.YELLOW}--help{Style.RESET_ALL}\n")


def main(argv=None):

    args = parse_args(argv)
    print(f"[DEBUG] Comando recibido: {args.command}")
    
    user_service = UserService(UserManager())
    role_service = RoleService()

    if args.command == "create":
        user_handler.handle_create_user(args, user_service)
    elif args.command == "delete":
        user_handler.handle_delete_user(args, user_service)
    elif args.command == "list-users":
        user_handler.handle_list_users(args, user_service)
    elif args.command == "search-user-id":
        user_handler.handle_list_user(args, user_service)
    elif args.command == "import":
        csv_handler.import_users_from_csv(args.csvfile)
    elif args.command == "list-roles":
        role_handler.handle_list_roles(args, role_service)
    elif not args.command:
        show_welcome()
    else:
        print(f"{Fore.RED}[X] Comando '{args.command}' no válido. Usa -h para ayuda.{Style.RESET_ALL}")





if __name__ == "__main__":
    show_welcome()
    launch_pro_cli(main)
