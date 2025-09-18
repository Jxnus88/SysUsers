"""
Módulo para gestionar usuarios en sistemas Linux.
Incluye funciones para crear, eliminar, buscar y listar usuarios.
"""

import subprocess
import pwd
from typing import Optional, List, Dict, Union

from exceptions import MissingGroupError, UserCreationError
from validators import ShellValidator
from managers.group_manager import GroupManager


class UserManager:
    
    def __init__(self):
        self.group_manager = GroupManager()
    """Clase encargada de operaciones relacionadas con usuarios."""

    def create_user(
        self,
        username: str,
        shell: str = "/bin/bash",
        temp_pass: Optional[str] = None,
        home: Optional[str] = None,
        groups: Optional[List[str]] = None
    ) -> None:
        """
        Crea un nuevo usuario en el sistema.

        Args:
            username (str): Nombre del nuevo usuario.
            shell (str): Shell asignado al usuario.
            temp_pass (Optional[str]): Contraseña temporal (opcional).
            home (Optional[str]): Ruta del directorio home (opcional).
            groups (Optional[List[str]]): Lista de grupos secundarios (opcional).

        Raises:
            MissingGroupError: Si uno de los grupos indicados no existe.
            UserCreationError: Si ocurre un error durante la creación del usuario.
        """

        ShellValidator.validate(shell)
        cmd = ['sudo', 'useradd', username]

        if home:
            cmd += ['-m', '-d', home]
        else:
            cmd.append('-m')

        cmd += ['-s', shell]

        if groups:
            clean_groups = [g.strip() for g in groups if g.strip()]
            for g in clean_groups:
                if not self.group_manager.group_exists(g):
                    raise MissingGroupError(g)
            cmd += ["-G", ','.join(clean_groups)]

        try:
            subprocess.run(cmd, check=True)

            if temp_pass:
                subprocess.run(
                    ['sudo', 'chpasswd'],
                    input=f"{username}:{temp_pass}".encode(),
                    check=True
                )
                subprocess.run(['sudo', 'chage', '-d', '0', username], check=True)

        except subprocess.CalledProcessError as e:
            raise UserCreationError(f"Error del sistema al crear el usuario: {e}")
        
    def group_exists(self, group_name: str) -> bool:
        """
        Verifica si un grupo existe en el sistema.

        Args:
            group_name (str): Nombre del grupo a verificar.

        Returns:
            bool: True si el grupo existe, False en caso contrario.
        """
        return self.group_manager.group_exists(group_name)
    
    def create_group(self, group_name:str) -> None:
        """
        Crea un grupo usando GroupManager.
        """
        self.group_manager.create_group(group_name)

    def delete_user(self, username: str) -> None:
        """
        Elimina un usuario del sistema.

        Args:
            username (str): Nombre del usuario a eliminar.

        Raises:
            Exception: Si ocurre un error durante la eliminación.
        """
        try:
            subprocess.run(['sudo', 'userdel', '-r', username], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error eliminando usuario: {e}")

    def list_all_users(self) -> List[Dict[str, Union[str, int]]]:
        """
        Lista todos los usuarios del sistema con UID >= 1000.

        Returns:
            List[Dict[str, Union[str, int]]]: Lista de diccionarios con datos de usuario.
        """
        users = []
        for user in pwd.getpwall():
            if user.pw_uid >= 1000 and 'nologin' not in user.pw_shell:
                users.append({
                    'username': user.pw_name,
                    'uid': user.pw_uid,
                    'home': user.pw_dir,
                    'shell': user.pw_shell
                })
        return users

    def get_user_by_uid(self, uid: int) -> Optional[Dict[str, Union[str, int]]]:
        """
        Obtiene información de un usuario por su UID.

        Args:
            uid (int): UID del usuario a buscar.

        Returns:
            Optional[Dict[str, Union[str, int]]]: Datos del usuario o None si no existe.
        """
        try:
            user = pwd.getpwuid(uid)
            return {
                'username': user.pw_name,
                'uid': user.pw_uid,
                'home': user.pw_dir,
                'shell': user.pw_shell
            }
        except KeyError:
            return None
