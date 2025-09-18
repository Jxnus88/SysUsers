from colorama import Fore, Style


def get_input(msg: str) -> str | None:
    valor = input(f"{msg} (o 'q' para cancelar): ").strip()
    if valor.lower() in ['q', 'volver']:
        print(f"{Fore.CYAN}[*] Operación cancelada por el usuario.{Style.RESET_ALL}\n")
        return None
    return valor