import pwd
from exceptions import UserAlreadyExists

class UserValidator:
    
    def __init__(self):
        pass
    
    def validate_user_not_exists(self, username:str):
        if self.user_exists(username):
            raise UserAlreadyExists(f"El usuario '{username}' ya existe.")
         
    @staticmethod
    def user_exists(username: str) -> bool:
        try:
            pwd.getpwnam(username)
            return True      
        except KeyError:
            return False