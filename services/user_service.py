import pwd, grp

from exceptions import MissingGroupError
from managers import RoleManager

class UserService:
    def __init__(self, user_manager):
        self.um = user_manager
        self.role_manager = RoleManager()
        
    
    def create_user(self,
                    username: str,
                    shell: str,
                    home: str | None,
                    groups: list[str] | None,
                    temp_pass: str,
                    role: str | None=None) -> None:
        group_list = []
        shell_to_use = shell
        
        if role:
            if not self.role_manager.role_exists(role):
                raise ValueError(f"El rol '{role}' no existe.")
            
            role_data = self.role_manager.get_role(role)
            group_list = role_data.get("groups", [])
            shell_to_use = role_data.get("default_shell") or shell
            
            # Crear grupos si no existen
            for group in group_list:
                if not self.um.group_exists(group):
                    self.um.create_group(group)
                    
        else:
            if groups:
                group_list = [g.strip() for g in groups if g.strip()]
                
                # Validación de grupos (aseguramos que existen)
                for group in group_list:
                    if not self.group_exists(group):
                        raise MissingGroupError(group)
            
        # Usamos UserManager para crear el usuario
        self.um.create_user(
            username=username,
            shell=shell_to_use,
            home=home,
            groups=group_list,
            temp_pass=temp_pass
        )
        
    def delete_user(self, username):
        self.um.delete_user(username)
        
    def list_users(self):
        users = self.um.list_all_users()
        all_groups = grp.getgrall()

        result = []
        for user in users:
            username = user['username']

            # Obtener grupos del usuario
            user_groups = [g.gr_name for g in all_groups if username in g.gr_mem or g.gr_gid == pwd.getpwnam(username).pw_gid]

            # Determinar rol por coincidencia
            role = self.role_manager.get_role_for_user(user_groups)

            result.append({
                **user,
                'groups': user_groups,
                'role': role
            })

        return result
    
    def get_user(self, uid):
        user = self.um.get_user_by_uid(uid)
        if not user:
            return None

        username = user['username']
        all_groups = grp.getgrall()

        # Obtener los grupos del usuario
        user_groups = [
            g.gr_name
            for g in all_groups
            if username in g.gr_mem or g.gr_gid == pwd.getpwnam(username).pw_gid
        ]

        # Determinar el rol
        role = self.role_manager.get_role_for_user(user_groups)

        return {
            **user,
            'groups': user_groups,
            'role': role
        }
    
    def create_group(self, group_name: str):
        """Crear grupo usando UserManager."""
        self.um.create_group(group_name)

    def group_exists(self, group_name: str) -> bool:
        """Verifica si el grupo existe usando UserManager."""
        return self.um.group_manager.group_exists(group_name)
