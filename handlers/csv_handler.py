import csv
from pathlib import Path

from colorama import Fore, Style
from managers import UserManager
from exceptions import InvalidShellError, MissingGroupError


REQUIRED_FIELDS = ['username', 'temp_pass']


def import_users_from_csv(file_path: str):
    um = UserManager()
    success = 0
    failed = 0

    file_path = Path(file_path).expanduser().resolve()

    if not file_path.exists():
        print(f"{Fore.RED}[X] Archivo no encontrado: {file_path}{Style.RESET_ALL}")
        print_sample_format()
        return

    try:
        with file_path.open(newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Validar cabecera obligatoria
            missing_required = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
            if missing_required:
                print(f"{Fore.RED}[X] El CSV no contiene los campos requeridos: {', '.join(missing_required)}{Style.RESET_ALL}")
                print_sample_format()
                return

            for idx, row in enumerate(reader, 1):
                username = row.get('username', '').strip()
                temp_pass = row.get('temp_pass', '').strip()
                shell = row.get('shell', '/bin/bash').strip() or '/bin/bash'
                home = row.get('home', '').strip() or None
                groups_raw = row.get('groups', '').strip()
                groups_list = [g.strip() for g in groups_raw.split(',') if g.strip()]

                if not username or not temp_pass:
                    print(f"{Fore.YELLOW}[!] Fila {idx} ignorada: 'username' y 'temp_pass' son obligatorios.{Style.RESET_ALL}")
                    failed += 1
                    continue

                print(f"{Fore.CYAN}[*] Creando usuario: {username}{Style.RESET_ALL}")

                try:
                    um.create_user(
                        username=username,
                        shell=shell,
                        home=home,
                        groups=groups_list,
                        temp_pass=temp_pass
                    )
                    print(f"{Fore.GREEN}[✓] Usuario '{username}' creado correctamente.{Style.RESET_ALL}")
                    success += 1

                except (InvalidShellError, MissingGroupError, ValueError) as e:
                    print(f"{Fore.RED}[X] Error creando usuario '{username}': {e}{Style.RESET_ALL}")
                    failed += 1

    except Exception as e:
        print(f"{Fore.RED}[X] Error durante la importación: {e}{Style.RESET_ALL}")
        return

    print(f"\n{Fore.YELLOW}Importación finalizada: {success} usuario(s) creados, {failed} con error.{Style.RESET_ALL}")


def print_sample_format():
    print(f"\n{Fore.CYAN}Formato esperado del CSV:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Campos obligatorios:{Style.RESET_ALL} username, temp_pass")
    print(f"{Fore.YELLOW}Campos opcionales:{Style.RESET_ALL} shell, home, groups\n")

    print(f"{Fore.WHITE}Ejemplo de contenido:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}username,temp_pass,shell,home,groups{Style.RESET_ALL}")
    print(f"{Fore.GREEN}jdoe,Segura123,/bin/bash,/home/jdoe,staff,dev{Style.RESET_ALL}")
    print(f"{Fore.GREEN}ana,Ana2023,/bin/zsh,/home/ana,admins{Style.RESET_ALL}")
    print(f"{Fore.GREEN}carlos,Carlit0s,,,/bin/bash,devops{Style.RESET_ALL}")

    print(f"\nPuedes subir el archivo desde cualquier ubicación de tu sistema (ej: Documentos, Escritorio).")
    print(f"Asegúrate de proporcionar la ruta completa o relativa correctamente.\n")
