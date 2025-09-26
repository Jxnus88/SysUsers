from exceptions import UidTooLowError


class UserIdValidator:
    
    def __init__(self):
        pass
    
    def user_id_validate(self, uid):
        
        if uid < 1000:
            raise UidTooLowError(f"Usuario: '{uid}' no se puede mostrar este usuario, solo se mostrarán usuarios que su UID es superior o igual a 1000.")