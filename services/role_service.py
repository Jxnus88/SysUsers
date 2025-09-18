from managers import RoleManager

class RoleService:
    def __init__(self):
        self.role_manager = RoleManager()
        
    def role_exists(self, role_name: str) -> bool:
        return self.role_manager.role_exists(role_name)
    
    def create_role(self,
                    role_name: str,
                    shell: str = "/bin/bash",
                    groups: list[str] = None):
        
        if self.role_exists(role_name):
            raise ValueError(f"El rol '{role_name}' ya existe.")
        
        self.role_manager.add_role(role_name, shell, groups or [])
        
        
    def modify_role(self,
                    role_name: str,
                    new_shell: str = None,
                    add_groups: list[str] = None,
                    remove_groups: list[str] = None,
                    replace_groups: list[str] = None):
        
        if not self.role_exists(role_name):
            raise ValueError(f"El rol '{role_name}' no existe.")
        
        self.role_manager.modify_role(
            role_name=role_name,
            new_shell=new_shell,
            add_groups=add_groups,
            remove_groups=remove_groups,
            replace_groups=replace_groups
        )
        
    def delete_role(self, role_name: str):
        if not self.role_exists(role_name):
            raise ValueError(f"El rol '{role_name}' no xiste.")
        
        self.role_manager.delete_role(role_name)
        
    def get_role_summary(self, role_name: str) -> dict:
        if not self.role_exists(role_name):
            raise ValueError(f"El rol '{role_name}' no existe.")
        
        data = self.role_manager.get_role_data(role_name)
        return {
            "shell": data.get("default_shell"),
            "groups": data.get("groups", [])
        }
    
    def list_roles(self) -> list[str]:
        return self.role_manager.list_roles()
    
    def get_role_data(self, role_name: str) -> dict:
        return self.role_manager.get_role_data(role_name)