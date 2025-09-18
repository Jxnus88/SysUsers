import json
import shutil

from pathlib import Path
from validators import RoleNotFoundError

try:
    import importlib.resources as pkg_resources  # Python 3.7+
except ImportError:
    import importlib.resources as pkg_resources  # backport para Python <3.7

class RoleManager:
    def __init__(self):
        # Ruta real editable del usuario
        self.user_roles_path = Path.home() / ".config" / "sysusers" / "roles.json"
        
        # Asegurar que el archivo existe (crear desde plantilla si es necesario)
        self._ensure_user_roles_file()
        
        # Cargar roles
        self.roles = self._load_roles()
        
    def _ensure_user_roles_file(self):
        """Crea ~/.config//sysusers/roles.json si no existe, copiándolo desde sysusers/data/roles.json"""
        if self.user_roles_path.exists():         
            return
        
        "Crea el directorio config si no existe"
        self.user_roles_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            base_path = Path(__file__).parent.parent  # Ajusta si la estructura es diferente
            template_path = base_path / "data" / "roles.json"
            if not template_path.exists():
                raise FileNotFoundError(f"No se encontró el archivo plantilla en {template_path}")
            shutil.copy(template_path, self.user_roles_path)
        except Exception as e:
            raise RuntimeError(f"Error al copiar roles.json template: {e}")

    def _load_roles(self):
        """Carga los roles desde el archivo .config"""
        if not self.user_roles_path.exists():
            raise FileNotFoundError("roles.json No se encuentra en la ruta de configuración de usuario esperada")
        try:
            with open(self.user_roles_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("roles.json solo contiene un objeto JSON (dicionario).")
                return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in roles.json: {e}")
        except FileNotFoundError:
            raise FileNotFoundError("roles.json No se encuentra en la ruta de configuración de usuario esperada")
        
    def _save_roles(self, roles_dict=None):
        """Guarda los roles del archivo .config"""
        roles_to_save = roles_dict or self.roles
        with open(self.user_roles_path, "w", encoding="utf-8") as f:
            json.dump(roles_to_save, f, indent=2)
        #print(f"[✓] roles.json guardado en {self.user_roles_path}")
        
    def reload_roles(self):
        """Recarga los roles desde el archivo"""
        self.roles = self._load_roles()
        
    def add_role(self, name: str, shell: str, groups: str):
        if self.role_exists(name):
            raise ValueError(f"El rol '{name}' ya existe.")
        if not isinstance(groups, list):
            raise ValueError("groups debe ser una lista")
        self.roles[name] = {
            "default_shell": shell,
            "groups": groups
        }
        self._save_roles()
        
    def modify_role(self, 
                    role_name: str, 
                    new_name: str=None,
                    new_shell: str =None, 
                    add_groups: list=None, 
                    remove_groups: list=None, 
                    replace_groups: list=None):
        
        if role_name not in self.roles:
            raise RoleNotFoundError(f"El rol '{role_name}' no existe.")
        role = self.roles[role_name]
        
        if "default_shell" not in role or "groups" not in role:
            raise ValueError(f"El rol '{role_name}' no tiene estructura válida.")

        if new_shell:
            role['default_shell'] = new_shell
        
        if replace_groups:
            role['groups']= list(set(replace_groups))
        
        if add_groups:
            role['groups'] = list(set(role['groups'] + add_groups))
        
        if remove_groups:
            role['groups'] = [g for g in role['groups'] if g not in remove_groups]
        
        # Renombrar rol si es necesario
        if new_name and new_name != role_name:
            self.roles[new_name] = role
            del self.roles[role_name]
        else:
            self.roles[role_name] = role
            
        self._save_roles()
    
    def delete_role(self, role_name:str):
        if role_name not in self.roles:
            raise RoleNotFoundError(f"El rol '{role_name}' no existe.")
        del self.roles[role_name]
        self._save_roles()
    
    def get_role(self, role_name):
        return self.roles.get(role_name)

    def get_role_data(self, role_name):
        role = self.get_role(role_name)
        if not role:
            raise ValueError(f"Role '{role_name}' no existe.")
        return role
    
    def role_exists(self, role_name):
        return role_name in self.roles
    
    def list_roles(self):
        return list(self.roles.keys())
    
    def get_role_for_user(self, user_groups: list[str]) -> str | None:
        for role_name, data in self.roles.items():
            expected_groups = set(data.get("groups", []))
            if expected_groups.issubset(user_groups):
                return role_name
        return None