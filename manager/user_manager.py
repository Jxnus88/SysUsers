import subprocess, pwd, grp, spwd

from datetime import datetime
from typing import Optional

from validators import (
    ShellValidator,
    HomeValidator,
    UserValidator,
    GroupValidator,
    PasswdValidator,
    UserIdValidator
    )
from exceptions import (
    UserCreationError,
    UserDoNotExists
    )

class UserManager:
    
    def __init__(self):
        self.user_validate = UserValidator()
        self.home_validate = HomeValidator()
        self.shell_validate = ShellValidator()
        self.group_validate = GroupValidator()
        self.passwd_validate = PasswdValidator()
        self.userid_validate = UserIdValidator()
    
    def create_user(self,
                    username: str,
                    home: str,
                    temp_pass: str,
                    list_groups: Optional[list[str]] = None,
                    shell: Optional[str] = "/bin/bash"
                    ) -> None:
        
        self.user_validate.validate_user_not_exists(username)
        self.home_validate.validate_home(home)
        
        if shell:
            self.shell_validate.validate_shell(shell)
            
        if list_groups:
            self.group_validate.validate_groups_exist(list_groups)
            
        self.passwd_validate.validate_passwd(temp_pass)
        
        
        cmd = ["sudo", "useradd", username]
        
        if home:
            cmd += ['-m', '-d', home]
        else:
            cmd.append('-m')
            
        cmd += ['-s', shell]
            
        if list_groups:
            group_str = ",".join(list_groups)
            cmd += ["-G", group_str]
            
        try:
            subprocess.run(
                cmd, 
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if temp_pass:
                subprocess.run(
                    ["sudo", "chpasswd"],
                    input=f"{username}:{temp_pass}".encode(),
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                subprocess.run(
                   ['sudo', 'chage', '-d', '0', username],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL 
                )
                 
        except subprocess.CalledProcessError as e:
            raise UserCreationError(f"No se pudo crear el usuario: {e}")
        
    def list_all_users(self):
        
        users = []
        for user in pwd.getpwall():
            if user.pw_uid >= 1000 and 'nologin' not in user.pw_shell:
                users.append({
                    'username':user.pw_name,
                    'uid':user.pw_uid,
                    'home':user.pw_dir,
                    'shell':user.pw_shell
                })
        
        return users
    
    def delete_user(self, uid:int) -> str:
        
        self.userid_validate.user_id_validate(uid)

        try:    
            user = pwd.getpwuid(uid)
        except KeyError as k:
            raise UserDoNotExists(f"No existe el usuario: {k}")
        
        username = user.pw_name
        gid = user.pw_gid
        
        group = grp.getgrgid(gid).gr_name
        
        home_delete = True
        group_delete = True
        
        try:
            subprocess.run(
                ['sudo', 'userdel', '-r', username], 
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            if e.returncode == 12:
                home_delete = False
                subprocess.run(
                    ['sudo', 'userdel', username], 
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            else:
                raise RuntimeError(f"Error al eliminar usuario: {e}")
        try:
            # Revisar si alguien más usa este grupo como su grupo principal
            group_in_use = any(
                user.pw_gid == gid and user.pw_name != username
                for user in pwd.getpwall()
            )
            
            # Revisar si hay miembros secundarios
            group_info = grp.getgrnam(group)
            has_secondary_members = len(group_info.gr_mem) > 0

            if not group_in_use and not has_secondary_members:
                
                try:
                    subprocess.run(
                        ['sudo', 'groupdel', group],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    group_delete = True
                    
                except subprocess.CalledProcessError:
                    group_delete = False
                    
            else:
                group_delete = False
        
        except KeyError:
            # Por si el grupo ya no existe
            group_delete = True
        
        return {
            "username":username,
            "status":"deleted",
            "home_deleted":home_delete,
            "group_deleted":group_delete
        }
        
    def get_user_id(self, uid: int) -> dict | None:
        self.userid_validate.user_id_validate(uid)

        try:
            user = pwd.getpwuid(uid)
            username = user.pw_name

            # Obteniendo la contraseña = True / False
            try:
                passwd_hash = spwd.getspnam(username).sp_pwdp
                
                if passwd_hash == '':
                    has_password = 'sin contraseña'
                
                elif passwd_hash.startswith('!') or passwd_hash.startswith('*'):
                    has_password = 'bloqueada'
                
                else:
                    has_password = 'si'
                
            except PermissionError:
                has_password = 'sin acceso'
            except KeyError as e:
                has_password = 'no existe usuario, comprueba si estas con tu cuenta de root.'
            

            # Última conexión del usuario
            last_login = 'Nunca ha accedido'
            try:
                result = subprocess.run(
                    ['last', username],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                output = result.stdout.strip()

                if output and "wtmp begins" not in output:
                    for line in output.splitlines():
                        if not line.strip() or username not in line:
                            continue

                        parts = line.split()
                        # Buscamos líneas con formato esperado: al menos 7 columnas (usuario, tty, host, día, mes, día, hora)
                        if len(parts) < 7:
                            continue

                        # Extraemos fecha y hora
                        date_str = ' '.join(parts[3:7])  # ejemplo: "Tue Sep 19 09:00"
                        try:
                            dt = datetime.strptime(date_str, "%a %b %d %H:%M")
                            dt = dt.replace(year=datetime.now().year)
                            last_login = dt.strftime("%Y-%m-%d %H:%M")
                            break  # Ya obtuvimos último login válido
                        except ValueError:
                            # Si falla el parseo, seguimos buscando en otras líneas
                            continue
                  
            except subprocess.CalledProcessError:
                last_login = None

            # Expiración de la cuenta
            password_expiry = None
            try:
                chage_result = subprocess.run(
                    ['chage', '-l', username],
                    capture_output=True,
                    text=True,
                    check=True
                )
                for line in chage_result.stdout.splitlines():
                    if line.startswith("Password expires"):
                        password_expiry = line.split(":", 1)[1].strip()
                        if password_expiry == "":
                            password_expiry = "Sin expiración"
                        break
            except subprocess.CalledProcessError:
                password_expiry = None

            # Retorno de todos los datos en diccionario
            return {
                'Nombre': username,
                'Uid': user.pw_uid,
                'Home': user.pw_dir,
                'Shell': user.pw_shell,
                'Tiene contraseña': has_password,
                'Última conexión': last_login or "Nunca ha accedido",
                'Expiración de contraseña': password_expiry or "Sin expiración"
            }
            
        except KeyError as e:
            raise UserDoNotExists(f"No existe el usuario: {e}")