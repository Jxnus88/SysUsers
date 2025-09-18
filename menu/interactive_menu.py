import sys
import time

from colorama import Fore, Style
from utils import get_input, clear_screen, next_step_menu

from managers import RoleManager, UserManager
from handlers import user_handler, csv_handler


class Args:
    pass


def show_menu():
    clear_screen()
    print(f"""{Fore.CYAN}
=== SYS USERS MENU ===
1. Crear usuario                    5. Importar usuarios desde csv
2. Eliminar usuario
3. Listar todos los usuarios
4. Consultar usuario por UID
0. Salir
{Style.RESET_ALL}""")
    
def menu_run():
    um = UserManager()
    
    while True:
        show_menu()
        choice = input(f"{Fore.YELLOW}[?] Selecciona una opción: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            while True:
                clear_screen()
                role_manager = RoleManager()
                
                username = get_input("Nombre del usuario: ")
                if username is None:
                    break
                
                use_role = get_input("¿Quieres asignar un rol predefinido? (s/n): ").lower()
                if use_role is None:
                    continue
                
                args = Args()
                args.username = username
                
                if use_role == 's':
                    print(f"{Fore.CYAN}[*] Roles disponibles:{Style.RESET_ALL}")
                    for role in role_manager.list_roles():
                        print(f" - {role}")
                        
                    selected_role = get_input("Escribe el nombre del rol: ")
                    if selected_role is None:
                        continue
                    
                    if not role_manager.role_exists(selected_role):
                        print(f"{Fore.RED}[X] El rol '{selected_role}' no existe.{Style.RESET_ALL}")
                        continue
                    
                    # Asigna valores desde el rol
                    role_data = role_manager.get_role(selected_role)
                    args.shell = role_data.get("default_shell", "/bin/bash")
                    args.groups = ",".join(role_data.get("groups", []))
                    
                    # Asigna Home por defecto
                    args.home = role_data.get("home", f"/home/{username}")
                    
                    # Pedimos contraseña temporal
                    args.temp_pass = get_input("Agregar una contraseña temporal: ")
                    if args.temp_pass is None:
                        continue
                else:
                    home_input = get_input("Home (vacío para usarlo por defecto /home/<usuario>): ")
                    if home_input is None:
                        continue
                    args.home = home_input.strip() if home_input.strip() else f"/home/{username}"
                    
                    shell_input = get_input("Shell (/bin/bash): ")
                    if shell_input is None:
                        continue
                    args.shell = shell_input.strip() if shell_input.strip() else "/bin/bash"
                    
                    use_custom_groups = get_input("¿Desea asignar grupos secundarios personalizados? (s/n): ").lower()
                    if use_custom_groups is None:
                        continue
                    
                    if use_custom_groups == 's':
                        groups = get_input("Grupos secundarios (separados por comas): ")
                        if groups is None:
                            continue
                        args.groups = groups if groups.strip() else None
                    else:
                        args.groups = None
                    
                    args.role = None
                    
                    # Pedimos la contraseña temporal al final, sea con rol o sin rol
                    temp_pass = get_input("Agregar una contraseña temporal (o 'q' para cancelar): ")
                    if temp_pass is None:
                        print(f"{Fore.CYAN}[*] Operación cancelada por el usuario.{Style.RESET_ALL}")
                        continue
                    args.temp_pass = temp_pass
                    
                # Mostrar resumen antes de crear el usuario
                print(f"\n{Fore.CYAN}Revisar la información del nuevo usuario:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Usuario:          {args.username}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Shell:            {args.shell}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Home:             {args.home}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Grupos:           {args.groups or 'Ninguno'}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Pass temporal:    {'*' * len(args.temp_pass)}{Style.RESET_ALL}")

                confirm = input(f"\n{Fore.GREEN}[?] ¿Deseas crear este usuario con los datos anteriores? (s/n): {Style.RESET_ALL}").strip().lower()
                if confirm != 's':
                    print(f"{Fore.RED}[X] Creación cancelada por el usuario.{Style.RESET_ALL}")
                    break  # Vuelve al menú o al flujo anterior

                user_handler.handle_create_user(args, um)
                
                next_step = next_step_menu(option1="Crear otro usuario")
                if next_step != '1':
                    clear_screen()
                    break
                                
        elif choice == '2':
            clear_screen()
            while True:
                username = get_input("Nombre del usuario a eliminar: ")
                if username is None:
                    break
                
                args = Args()
                args.username = username
                
                user_handler.handle_delete_user(args, um)
                
                next_step = next_step_menu(option1="Eliminar otro usuario")
                if next_step != '1':
                    clear_screen()
                    break 
                
                clear_screen()
            
        elif choice == '3':
            clear_screen()
            user_handler.handle_list_users(None, um)
            input(f"{Fore.YELLOW}\n[!] Presiona Enter para volver al menú...{Style.RESET_ALL}")
            
        elif choice == '4':
            clear_screen()
            try:
                uid_input = get_input("UID del usuario: ")
                if uid_input is None:
                    continue
                
                args = Args()
                args.uid = int(uid_input)
                user_handler.handle_list_user(args, um)
                
            except ValueError:
                print(f"{Fore.RED}[X] UID inválido.{Style.RESET_ALL}")
                
        
        elif choice == '5':
            clear_screen()
            file_path = get_input("Ruta al archivo CSV: ")
            if file_path is None:
                continue
            
            csv_handler.import_users_from_csv(file_path)
            
            input(f"{Fore.YELLOW}\n[!] Presiona Enter para volver al menú...{Style.RESET_ALL}")

        elif choice == '0':
            print(f"{Fore.CYAN}[*] Saliendo del menú...{Style.RESET_ALL}")
            time.sleep(1.5)
            clear_screen()
            sys.exit()
            
        else:
            print(f"{Fore.RED}[X] Opción inválida. Intenta de nuevo.{Style.RESET_ALL}")


if __name__ == "__main__":
    menu_run()