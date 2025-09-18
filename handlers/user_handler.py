from colorama import Fore, Style
from utils import (
    get_available_shells,
    next_step_menu,
    clear_screen,
    get_input
)
from exceptions import InvalidShellError, MissingGroupError
import menu.cli as app_cli



def handle_create_user(args, user_service):
    while True:
        try:
            user_service.create_user(
                username=args.username,
                shell=args.shell,
                home=args.home,
                groups=args.groups.split(",") if args.groups else [],
                temp_pass=args.temp_pass,
                role=args.role if hasattr(args, "role") else None
            )

            print(f"{Fore.GREEN}[✓] Usuario '{args.username}' creado correctamente.{Style.RESET_ALL}")
            break
        
        except InvalidShellError as isd:
            print(f"{Fore.RED}[X] Error: {isd}{Style.RESET_ALL}")
            
            shells = get_available_shells()

            print(f"{Fore.CYAN}[*] Shells disponibles en este sistema:{Style.RESET_ALL}")
            for idx, sh in enumerate(shells, start=1):
                print(f"{idx}. {sh}")
            
            choice = input(f"{Fore.YELLOW}[?] Elige el número de la shell deseada o 'n' para cancelar: {Style.RESET_ALL}").strip()
            if choice.lower() == 'n':
                print(f"{Fore.RED}[X] Proceso cancelado por el usuario.{Style.RESET_ALL}")
                break
            
            try:
                choice_idx = int(choice) - 1
                args.shell = shells[choice_idx]
            except (ValueError, IndexError):
                print(f"{Fore.RED}[X] Selección inválida. Cancelando...{Style.RESET_ALL}")
                break
            
        except MissingGroupError as mge:
            group = mge.group_name.strip()
            response = input(f"{Fore.YELLOW}[?] El grupo '{group}' no existe. ¿Deseas crearlo? (s/n): {Style.RESET_ALL}").strip().lower()
            if response == 's':
                try:
                    user_service.um.create_group(group)
                    print(f"{Fore.CYAN}[+] Grupo '{group}' creado.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[X] Error al crear el grupo: {e}{Style.RESET_ALL}")
                    break
            else:
                print(f"{Fore.RED}[X] Usuario no creado. Grupo '{group}' requerido.{Style.RESET_ALL}")
                break
            
        except ValueError as ve:
            print(f"{Fore.YELLOW}[!] {ve}{Style.RESET_ALL}")
            break
        
        except Exception as e:
            print(f"{Fore.RED}[X] Error inesperado: {e}{Style.RESET_ALL}")
            break
        
def handle_delete_user(args, user_service):
    confirm = input(f"{Fore.YELLOW}[?] ¿Estás seguro de que quieres eliminar al usuario '{args.username}'? (s/n): {Style.RESET_ALL}").strip().lower()
    if confirm != 's':
        print(f"{Fore.CYAN}[*] Operación cancelada.{Style.RESET_ALL}")
        return
    
    try:
        user_service.delete_user(args.username)
        print(f"{Fore.GREEN}[✓] Usuario '{args.username}' eliminado correctamente.{Style.RESET_ALL}")
    except Exception:
        print(f"{Fore.RED}[X] No se pudo eliminar el usuario. Asegúrate de que existe y que tienes permisos suficientes.{Style.RESET_ALL}")

def handle_list_users(args, user_service):
    users = user_service.list_users()
    if not users:
        print(f"{Fore.YELLOW}[!] No se encontraron usuarios.{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}\n[*] Lista de usuarios del sistema:{Style.RESET_ALL}")
    print(f"{'-'*120}")
    print(f"{'Usuario':<15}{'UID':<10}{'Home':<25}{'Shell':<20}{'Grupos':<30}{'Rol'}")
    print(f"{'-'*120}")
    
    for u in users:
        grupos = ','.join(u.get('groups', []))
        rol = u.get('role') or '-'
        print(f"{u['username']:<15}{u['uid']:<10}{u['home']:<25}{u['shell']:<20}{grupos:<30}{rol}")
         
    print(f"{'-'*120}\n")
    print(f"{Fore.CYAN}[*] Total de usuarios listados: {len(users)}{Style.RESET_ALL}\n")


def handle_list_user(args, user_service):
    while True:
        try:
            # Paso 1: Validar el UID de entrada
            uid_str = str(args.uid) if hasattr(args, 'uid') and args.uid is not None else get_input("UID del usuario: ")

            if uid_str is None:
                clear_screen()
                return

            if not uid_str.isdigit():
                raise ValueError("UID inválido. Debe ser un número entero.")

            uid = int(uid_str)

            # Paso 2: Obtener datos del usuario
            user = user_service.get_user(uid)
            if not user:
                print(f"{Fore.RED}[X] No se encontró ningún usuario con UID {uid}.{Style.RESET_ALL}")
                return

            # Paso 3: Imprimir información
            grupos = ', '.join(user.get('groups', []))
            rol = user.get('role') or '-'

            print(f"{Fore.CYAN}[*] Información del usuario UID {uid}:{Style.RESET_ALL}")
            print(f"{'-'*120}")
            print(f"{'Usuario':<15}{'UID':<10}{'Home':<25}{'Shell':<20}{'Grupos':<30}{'Rol'}")
            print(f"{'-'*120}")
            print(f"{user['username']:<15}{user['uid']:<10}{user['home']:<25}{user['shell']:<20}{grupos:<30}{rol}")
            print(f"{'-'*120}\n")

            # Paso 4: Siguiente acción
            next_step = next_step_menu(option1="Comprobar información de otro usuario")
            if next_step == '1':
                clear_screen()
                args.uid = None  # Reiniciar UID para nuevo ciclo
                continue
            else:
                clear_screen()
                app_cli.show_welcome()
                break

        except ValueError as ve:
            print(f"{Fore.RED}[X] {ve}{Style.RESET_ALL}")
            args.uid = None  # Permitir reintento
            continue
        except Exception as e:
            print(f"{Fore.RED}[X] Error inesperado: {e}{Style.RESET_ALL}")
            break

