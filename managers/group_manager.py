"""
Gestión de grupos del sistema Linux.

Este módulo permite verificar si un grupo existe y crearlo si es necesario.
"""

import subprocess

class GroupManager:
    """Clase para gestionar grupos del sistema."""

    @staticmethod
    def group_exists(group_name: str) -> bool:
        """
        Verifica si un grupo existe en el sistema.

        Args:
            group_name (str): Nombre del grupo a verificar.

        Returns:
            bool: True si el grupo existe, False en caso contrario.
        """
        result = subprocess.run(
            ["getent", "group", group_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0

    @staticmethod
    def create_group(group_name: str) -> None:
        """
        Crea un nuevo grupo en el sistema.

        Args:
            group_name (str): Nombre del grupo a crear.

        Raises:
            RuntimeError: Si falla la creación del grupo.
        """
        try:
            subprocess.run(['sudo', 'groupadd', group_name], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error al crear el grupo '{group_name}': {e}")
