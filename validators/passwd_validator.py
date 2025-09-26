from exceptions import NotPasswdError


class PasswdValidator:
    
    def __init__(self):
        pass
    
    def validate_passwd(self, passwd:str) -> None:
        if not passwd or not passwd.strip():
            raise NotPasswdError("Contraseña no proporcionada.")