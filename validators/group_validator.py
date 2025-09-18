import grp
from exceptions.group_errors import MissingGroupError

class GroupValidator:
    @staticmethod
    def validate(groups: list[str]) -> None:
        """
        Valida que todos los grupos existen en el sistema.
        Lanza MissingGroupError con el primer grupo no encontrado.
        """
        for group in groups:
            group = group.strip()
            if not group:
                continue
            try:
                grp.getgrnam(group)
            except KeyError:
                raise MissingGroupError(group)
