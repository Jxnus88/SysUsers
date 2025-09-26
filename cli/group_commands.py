from tabulate import tabulate
from colorama import Fore, Style

from exceptions import (
    NotExistGroupError,
    GroupAlreadyExistsError,
    InvalidGroupNameError,
    GroupModificationError,
    GroupDeletionError,
    GroupCreationError
)

from manager import GroupManager
from loggin.logger import get_logger

GM = GroupManager()
logger = get_logger(to_console=False)

def create_group(args):
    
    try:
        GM.create_group(
            namegroup=args.groupname
        )
        print(f"{Fore.GREEN}[✓] Grupo '{args.groupname}' creado correctamente.{Style.RESET_ALL}")
        logger.info(f"Grupo '{args.groupname}' creado correctamente.")
        
    except GroupAlreadyExistsError as gae:
        print(f"{Fore.YELLOW}[!] El grupo '{args.groupname}' ya existe en el sistema.")
        logger.info(gae)
    
    except InvalidGroupNameError as ign:
        print(f"{Fore.YELLOW}[!] Debes introducir un nombre para el grupo.{Style.RESET_ALL}")
        logger.error(ign)
        
    except GroupCreationError as gce:
        print(f"{Fore.RED}[X] No se pudo crear el grupo '{args.groupname}'.{Style.RESET_ALL}")
        logger.error(gce)

    except ValueError as ve:
        print(f"{Fore.YELLOW}[!] Error de parámetro: {ve}{Style.RESET_ALL}")
        logger.error(ve)
    
    except Exception as e:
        print(f"{Fore.RED}[X] Error inesperado: {e}{Style.RESET_ALL}")
        logger.exception(e)
        
def create_groups(args):
    
    try:
        created = []
        skipped = []

        for group in args.groups:
            try:
                GM.create_groups(group)
                created.append(group)
                print(f"{Fore.GREEN}[✓] Grupo '{group}' creado correctamente.{Style.RESET_ALL}")
                logger.info(f"Grupo ¡{group}' creado.")
                
            except GroupAlreadyExistsError:
                skipped.append(group)
                print(f"{Fore.YELLOW}[!] El grupo '{group}' ya existe. Se omitió.{Style.RESET_ALL}")
                logger.warning(f"Intento de crear grupo existente: '{group}'")
        
        if not created:
            logger.info("No se creó ningún grupo nuevo.")      
        else:
            logger.info(f"Grupos creados: {created}")
            
    except Exception as e:
        print(f"{Fore.RED}[X] Error inesperado: {e}{Style.RESET_ALL}")
        logger.exception("Error inesperado al crear grupos.")

def list_groups(args):
    
    try:
        groups = GM.list_groups()
        
        if not groups:
            print(f"{Fore.YELLOW}[!] No hay grupos registrados.{Style.RESET_ALL}")
            logger.info("No se encontraron grupos registrados en el sistema.")
            return
        
        headers = [
            f"{Fore.CYAN}Grupo{Style.RESET_ALL}",
            f"{Fore.CYAN}GID{Style.RESET_ALL}",
            f"{Fore.CYAN}Miembros{Style.RESET_ALL}",
            f"{Fore.CYAN}Tipo{Style.RESET_ALL}"
        ]
        
        rows = []
        
        for group in groups:
            type_group = group["type"]
            type_colored = type_group
            type_colored = (
                f"{Fore.GREEN}{type_colored}{Style.RESET_ALL}"
                if type_group == "usuario" else
                f"{Fore.MAGENTA}{type_colored}{Style.RESET_ALL}"
            )
            rows.append([
                group["name"],
                group["gid"],
                group["members"],
                type_colored
            ])
            
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        logger.info(f"Consulta de grupos del sistema: {len(groups)} grupos listados.")
        
    except Exception as e:
        print(f"{Fore.RED}[X] Error al listar los grupos: {e}{Style.RESET_ALL}")
        logger.exception("Error inesperado al listar los grupos.")
        
def search_group_name(args):
    
    try:
        results = GM.search_group_name(args.groupname)
        
        if not results:
            print(f"{Fore.YELLOW}[!] No se encontraron resultados para el grupo '{args.name}'.{Style.RESET_ALL}")
            return
        
        rows = []
        for group in results:
            members = group["members"]
            if not members:
                members = "Sin miembros"
            else:
                members = ", ".join(members)

            rows.append([
                group["name"],
                group["gid"],
                members,
                group["type"]
            ])
        
        headers = [
            f"{Fore.CYAN}Nombre{Style.RESET_ALL}",
            f"{Fore.CYAN}GID{Style.RESET_ALL}",
            f"{Fore.CYAN}Miembros{Style.RESET_ALL}",
            f"{Fore.CYAN}Tipo{Style.RESET_ALL}"
        ]

        
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        logger.info(f"Consulta de grupo por nombre: {args.groupname}")
        
    except NotExistGroupError:
        print(f"{Fore.YELLOW}[!] No se encontró ningún grupo con el nombre {args.groupname}")
                
    except Exception as e:
        print(f"{Fore.RED}[X] Error inesperado: {e}{Style.RESET_ALL}")
        logger.exception("Error inesperado al buscar grupo por nombre.")
      
def modify_group(args):
    
    confirm = input(f"{Fore.YELLOW}[?] ¿Seguro que deseas renombrar '{args.current_name}' a '{args.new_name}'? (s/N): {Style.RESET_ALL}").strip().lower()
    if confirm != 's':
        print(f"{Fore.CYAN}[*] Operación cancelada. Grupo no renombrado.{Style.RESET_ALL}")
        return
    
    try:
        GM.modify_group(args.current_name, args.new_name)
        print(f"{Fore.GREEN}[✓] Grupo '{args.current_name}' renombrado a '{args.new_name}'.{Style.RESET_ALL}")
        logger.info(f"Grupo renombrado: '{args.current_name}' → '{args.new_name}'")
    
    except NotExistGroupError as nge:
        print(f"{Fore.RED}[X] El grupo '{args.current_name}' no existe.{Style.RESET_ALL}")
        logger.warning(f"Intento de modificar grupo inexistente: {args.current_name}")

    except GroupAlreadyExistsError as gae:
        print(f"{Fore.YELLOW}[!] Ya existe un grupo con el nombre '{args.new_name}'.{Style.RESET_ALL}")
        logger.warning(f"{gae}")

    except GroupModificationError as gme:
        print(f"{Fore.RED}[X] No se pudo modificar el grupo: {gme}{Style.RESET_ALL}")
        logger.error(f"Fallo al modificar grupo '{args.current_name}' → '{args.new_name}': {gme}")

    except Exception as e:
        print(f"{Fore.RED}[X] Error inesperado: {e}{Style.RESET_ALL}")
        logger.exception("Error inesperado al modificar grupo.")
        
def delete_group(args):
    
    confirm = input(f"{Fore.YELLOW}[?] ¿Estás seguro de que quieres eliminar el grupo '{args.groupname}'? (s/N): {Style.RESET_ALL}").strip().lower()
    if confirm != 's':
        print(f"{Fore.CYAN}[*] Operación cancelada. Grupo no eliminado.{Style.RESET_ALL}")
        logger.info(f"Grupo '{args.groupname}' no eliminado.")
        return
    try:
        result = GM.delete_group(args.groupname)
        print(f"{Fore.GREEN}[✓] Grupo '{args.groupname}' eliminado correctamente.{Style.RESET_ALL}")
        logger.warning(f"El grupo '{args.groupname}' ha sido eliminado.")
    
    except NotExistGroupError as nege:
        print(f"El grupo '{args.groupname}' no existe en el sistema.")
        logger.error(nege)

    except GroupDeletionError as gde:
        print(f"No se pudo eliminar el grupo '{args.groupname}'.")
        logger.error(gde)
    
    except Exception as e:
        print(f"{Fore.RED}[X] Error inesperado al eliminar el grupo: {e}{Style.RESET_ALL}")
        logger.exception("Error inesperado al eliminar el grupo: {e}")