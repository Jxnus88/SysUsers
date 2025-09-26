from colorama import Fore, Style

def show_manual():
    """Muestro toda la información detallada del CLI."""

    print(f"\n{Fore.WHITE}Modo Profesional (CLI interactiva):{Style.RESET_ALL}")
    print(f"  En este modo puedes escribir directamente los comandos sin 'sysusers.cli' delante.")
    print(f"  Ejemplo de comandos que puedes escribir:")
    print(f"    {Fore.YELLOW}list-users{Style.RESET_ALL}")
    print(f"    {Fore.YELLOW}[!] Importante: en --groups usar solo comas para separar, sin espacios. Ejemplo: --groups staff,admin{Style.RESET_ALL}")
    print(f"    {Fore.YELLOW}create pedro --shell /bin/bash --groups staff,users --temp-pass Pedro123{Style.RESET_ALL}")
    print(f"    {Fore.YELLOW}delete pedro{Style.RESET_ALL}")
    print(f"    {Fore.YELLOW}search-user-id 1001{Style.RESET_ALL}")
    print(f"\n  Escribe 'exit' o 'quit' para salir del modo CLI profesional.\n")

    print(f"{Fore.WHITE}Uso básico para crear usuario (línea de comandos estándar):{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}create pedro --shell /bin/bash --home /home/pedro --groups staff,users --temp-pass Pedro123{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Otros comandos disponibles (modo estándar):{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}create{Style.RESET_ALL}            - Crear un usuario")
    print(f"  {Fore.CYAN}delete{Style.RESET_ALL}            - Eliminar un usuario")
    print(f"  {Fore.CYAN}list-users{Style.RESET_ALL}        - Listar todos los usuarios")
    print(f"  {Fore.CYAN}search-user-id{Style.RESET_ALL}    - Buscar usuario por UID")

    print(f"\n{Fore.WHITE}Comandos para gestionar grupos:{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}create-group{Style.RESET_ALL}         - Crear un grupo")
    print(f"  {Fore.CYAN}create-groups{Style.RESET_ALL}        - Crear múltiples grupos")
    print(f"  {Fore.CYAN}list-groups{Style.RESET_ALL}          - Listar todos los grupos")
    print(f"  {Fore.CYAN}search-group-name{Style.RESET_ALL}    - Buscar grupo por nombre")
    print(f"  {Fore.CYAN}modify-group{Style.RESET_ALL}         - Modificar nombre de un grupo")
    print(f"  {Fore.CYAN}delete-group{Style.RESET_ALL}         - Eliminar un grupo")

    print(f"\n{Fore.WHITE}Ejemplos para gestión de grupos:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}create-group developers{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}create-groups devops infra backend{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}list-groups{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}search-group-name devops{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}modify-group devops plataforma{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}delete-group infra{Style.RESET_ALL}")

    print(f"\n{Fore.WHITE}Ejemplos de ayuda con comandos:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}create -h{Style.RESET_ALL}         Muestra ayuda para crear usuarios")
    print(f"  {Fore.YELLOW}delete -h{Style.RESET_ALL}         Muestra ayuda para eliminar usuarios")
    print(f"\nPara más opciones usa: {Fore.YELLOW}-h{Style.RESET_ALL} o {Fore.YELLOW}--help{Style.RESET_ALL}\n")
