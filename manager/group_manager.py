import subprocess
from typing import Optional
from validators import GroupValidator
from exceptions import (
    NotExistGroupError,
    GroupAlreadyExistsError,
    GroupModificationError,
    GroupDeletionError,
    GroupCreationError
)


class GroupManager:

    def __init__(self):
        self.group_validate = GroupValidator()

    def _search_group(self, groupname: Optional[str] = None) -> list[dict]:
        cmd = ['getent', 'group']
        
        if groupname is not None:
            cmd.append(groupname)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError:
            if groupname:
                raise NotExistGroupError(f"El grupo '{groupname}' no existe.")
            else:
                raise RuntimeError(f"El grupp '{groupname}' no exite.")

        lines = result.stdout.strip().split('\n')
        groups = []

        for line in lines:
            parts = line.split(':')

            if len(parts) >= 4:
                name = parts[0]
                gid = parts[2]
                members = parts[3].split(',') if parts[3] else None
                group_type = "usuario" if int(gid) >= 1000 else "sistema"
                groups.append({
                    "name": name,
                    "gid": gid,
                    "members": members,
                    "type": group_type
                })

        return groups

    def create_group(self, namegroup: str) -> None:
        self.group_validate.validate_group_does_not_exist(namegroup)

        try:
            subprocess.run(["sudo", "groupadd", namegroup], check=True)
        except subprocess.CalledProcessError as e:
            raise GroupCreationError(f"No se pudo crear el grupo '{namegroup}': {e}")


    def create_groups(self, groups: list[str]) -> None:
        for group in groups:
            try:
                self.create_group(group)
            except GroupAlreadyExistsError:
                raise GroupAlreadyExistsError("Alguno de los grupos ya existen en el sistema.")

    def list_groups(self) -> list[dict]:
        return self._search_group()

    def search_group_name(self, groupname: str) -> list[dict]:
        return self._search_group(groupname)

    def modify_group(self, current_name: str, new_name: str) -> None:
        self.group_validate.validate_group_exists(current_name)

        try:
            self.group_validate.validate_group_does_not_exist(new_name)
        except GroupAlreadyExistsError:
            raise GroupAlreadyExistsError(f"Ya existe un grupo con el nombre '{new_name}'.")

        try:
            subprocess.run(
                ["sudo", "groupmod", "-n", new_name, current_name],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            raise GroupModificationError(
                f"No se pudo modificar el grupo '{current_name}' a '{new_name}': {e}"
            )

    def delete_group(self, groupname: str) -> None:
        self.group_validate.validate_group_exists(groupname)

        try:
            subprocess.run(
                ["sudo", "groupdel", groupname],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            raise GroupDeletionError(
                f"No se pudo eliminar el grupo '{groupname}': {e}"
            )
