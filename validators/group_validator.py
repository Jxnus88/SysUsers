import grp

from exceptions import (
    NotExistGroupError,
    GroupAlreadyExistsError,
    InvalidGroupNameError
    )

class GroupValidator:
    
    def __init__(self):
        pass

    def _sanitize_group(self, group: str) -> str:
        group = group.strip()
        
        if not group:
            raise InvalidGroupNameError("El nombre del grupo no puede estar vacío.")
        return group
    
    def validate_group_exists(self, group: str) -> None:
        group = self._sanitize_group(group)
        
        try:
            grp.getgrnam(group)
            
        except KeyError:
            raise NotExistGroupError(f"El grupo '{group}' no existe")
        
    def validate_group_does_not_exist(self, group: str) -> None:
        group = self._sanitize_group(group)
        
        try:
            grp.getgrnam(group)
            raise GroupAlreadyExistsError(f"El grupo '{group}' ya existe.")
        
        except KeyError:
            pass
        
    def validate_groups_exist(self, groups: list[str]) -> None:
        grupos_invalidos = []

        for group in groups:
            try:
                self.validate_group_exists(group)
            except NotExistGroupError:
                grupos_invalidos.append(group)

        if grupos_invalidos:
            raise NotExistGroupError(
                f"Los siguientes grupos no existen: {', '.join(grupos_invalidos)}, debes revisar los grupos disponibles en el sistema."
            )

            