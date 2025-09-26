

class GroupError(Exception):
    """Excepción base para errores relacionados con grupos del sistema."""
    pass

class NotExistGroupError(GroupError):
    """Se lanza cuando un grupo especificado no existe en el sistema."""
    pass

class GroupAlreadyExistsError(GroupError):
    """Se lanza cuando el grupo que se intenta crear y ya existe."""
    pass

class InvalidGroupNameError(GroupError):
    """Se lanza cuando el nombre del grupo está vacío o inválido."""
    pass

class GroupModificationError(GroupError):
    """Se lanza cuando ocurre un error al modificar un grupo."""
    pass

class GroupDeletionError(GroupError):
    """Se lanza cuando ocurre un error al eliminar un grupo."""
    pass

class GroupCreationError(GroupError):
    """Se lanza cuando hay un error al crear el grupo"""