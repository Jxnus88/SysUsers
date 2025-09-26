import pwd

from tabulate import tabulate
from colorama import Fore, Style

from exceptions import (
    UserAlreadyExists,
    UserDoNotExists,
    UserCreationError,
    NotExistGroupError,
    InvalidShellError,
    NotPasswdError
)
from manager import UserManager
from validators import ShellValidator
from loggin.logger import get_logger


logger = get_logger(to_console=False)
UM = UserManager()
VALID_SHELLS = ShellValidator()

def create_user(args):
    
    try:
        list_groups = [g.strip() for g in args.groups.split(',')] if args.groups else None

        UM.create_user(
            username=args.username, 
            home=args.home, 
            temp_pass=args.temp_pass, 
            list_groups=list_groups,
            shell=args.shell
            )
        
        print(f"{Fore.GREEN}[✓] Usuario '{args.username}' creado correctamente.{Style.RESET_ALL}")
        logger.info(f"Usuario '{args.username}' creado correctamente.")
        
    except UserAlreadyExists as uae:
        print(f"{Fore.YELLOW}[!] El nombre del usuario '{args.username}' ya existe en el sistema.")
        logger.error(uae)
    
    except InvalidShellError as ise:
        print(f"{Fore.YELLOW}[!] Nota: La shell especificada no es válida.{Style.RESET_ALL}")
        logger.error(ise)
        
    except NotExistGroupError as nege:
        print(f"{Fore.YELLOW}[!] {nege}{Style.RESET_ALL}")
        logger.error(nege)
        
    except NotPasswdError as npe:
        print(f"{Fore.YELLOW}[!] Debe proporcionar una contraseña.{Style.RESET_ALL}") 
        logger.error(npe)  
        
    except UserCreationError as uce:
        print(f"{Fore.RED}[X] No se ha podido crear al usuario '{args.username}'.{Style.RESET_ALL}") 
        logger.error(uce)
        
    except ValueError as ve:
        print(f"{Fore.YELLOW}[!] Error de parámetro: {ve}{Style.RESET_ALL}")
        logger.error(ve)

    except Exception as e:
        print(f"{Fore.RED}[X] Error inesperado: {e}{Style.RESET_ALL}")
        logger.exception(e)
    
def search_user_id(args):
    
    try:
        result = UM.get_user_id(args.uid)   
        
        headers = [
            f"{Fore.CYAN}Nombre{Style.RESET_ALL}",
            f"{Fore.CYAN}UID{Style.RESET_ALL}",
            f"{Fore.CYAN}Home{Style.RESET_ALL}",
            f"{Fore.CYAN}Shell{Style.RESET_ALL}",
            f"{Fore.CYAN}Tiene contraseña{Style.RESET_ALL}",
            f"{Fore.CYAN}Última conexión{Style.RESET_ALL}",
            f"{Fore.CYAN}Expiración de contraseña{Style.RESET_ALL}"
        ]
        
        shell = result["Shell"]
        try:
            VALID_SHELLS.validate_shell(shell)
            shell_colored = f"{Fore.GREEN}{shell}{Style.RESET_ALL}"
        except InvalidShellError:
            shell_colored = f"{Fore.RED}{shell}{Style.RESET_ALL}"
        
        row = [[
            result['Nombre'],
            result['Uid'],
            result['Home'],
            shell_colored,
            f"{Fore.GREEN}Sí{Style.RESET_ALL}" if result['Tiene contraseña'] else f"{Fore.RED}No{Style.RESET_ALL}",
            result['Última conexión'],
            result['Expiración de contraseña']
        ]]
        
        print(tabulate(row, headers=headers, tablefmt="fancy_grid"))
        logger.info(f"Consulta de usuario por UID: {result["Uid"]} - {result["Nombre"]}")
        
    except UserDoNotExists:
        print(f"{Fore.YELLOW}[!] No se encontró ningún usuario con UID {args.uid}.{Style.RESET_ALL}")
        logger.warning(f"No se encontró usuario con UID {args.uid}")
        
    except Exception as e:
        print(f"{Fore.RED}[X] Error inesperado: {e}{Style.RESET_ALL}")
        logger.exception("Error inesperado al buscar usuario por UID")

def list_users(args):

    try:
        users = UM.list_all_users()
        
        if not users:
            print(f"{Fore.YELLOW}[!] No hay usuarios registrados.{Style.RESET_ALL}")
            logger.info("No se encontraron usuarios en el sistema.")
            return
        
        headers = [
            f"{Fore.CYAN}Usuario{Style.RESET_ALL}",
            f"{Fore.CYAN}UID{Style.RESET_ALL}",
            f"{Fore.CYAN}Home{Style.RESET_ALL}",
            f"{Fore.CYAN}Shell{Style.RESET_ALL}"
        ]
        
        table = []
        
        for user in users:
            shell = user["shell"]
            try:
                VALID_SHELLS.validate_shell(shell)
                shell_colored = f"{Fore.GREEN}{shell}{Style.RESET_ALL}"
            except InvalidShellError:
                shell_colored = f"{Fore.RED}{shell}{Style.RESET_ALL}"

            table.append([
                user["username"],
                user["uid"],
                user["home"],
                shell_colored
            ])
        
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        logger.info(f"Consulta de usuarios del sistema: {len(users)} usuarios listados.")
    
    except Exception as e:
        print(f"{Fore.RED}[X] Error al listar usuarios: {e}{Style.RESET_ALL}")
        logger.exception("Error inesperado al listar usuarios.")

def delete_user(args):
    input_value = args.username  # puede ser username o UID como string

    confirm = input(f"{Fore.YELLOW}[?] ¿Estás seguro de que quieres eliminar al usuario '{input_value}'? (s/N): {Style.RESET_ALL}").strip().lower()
    if confirm != 's':
        print(f"{Fore.CYAN}[*] Operación cancelada. Usuario no eliminado.{Style.RESET_ALL}")
        logger.info(f"Usuario '{input_value}' no eliminado.")
        return

    try:
        # Detectar si input es UID (número)
        if input_value.isdigit():
            uid = int(input_value)
            user_info = pwd.getpwuid(uid)
        else:
            user_info = pwd.getpwnam(input_value)
            uid = user_info.pw_uid

        result = UM.delete_user(uid)
        print(f"{Fore.GREEN}[✓] Usuario '{result['username']}' eliminado correctamente.{Style.RESET_ALL}")
        logger.warning(f"El usuario '{result['username']}' ha sido eliminado.")

    except KeyError:
        print(f"{Fore.RED}[X] El usuario '{input_value}' no existe en el sistema.{Style.RESET_ALL}")
        logger.error(f"Usuario '{input_value}' no existe.")
    
    except UserDoNotExists as udne:
        print(f"{Fore.RED}[X] {udne}{Style.RESET_ALL}")
        logger.error(udne)
    
    except Exception as e:
        print(f"{Fore.RED}[X] Error inesperado al eliminar usuario: {e}{Style.RESET_ALL}")
        logger.exception(f"Error inesperado al eliminar usuario: {e}")

        