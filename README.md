# SysUsers - Administrador de Usuarios para Linux

SysUsers es una herramienta de línea de comandos para la gestión de usuarios y grupos en sistemas Linux. Permite crear, eliminar, listar y buscar usuarios y grupos, así como modificar grupos existentes.

---

## Requisitos y Consideraciones Previas

- Debes ejecutar los comandos **desde dentro de la carpeta donde está descargado el proyecto**.  
- Es necesario usar la aplicación como **root** o con permisos de administrador, ya que algunas operaciones requieren permisos elevados.  
- Se recomienda crear y activar un **entorno virtual de Python** antes de usar la aplicación para manejar dependencias de manera aislada.

---

## Comandos Disponibles

### Gestión de Usuarios

- `create <username> --temp-pass <password> [--shell <shell>] [--home <home_directory>] [--groups <group1,group2,...>]`  
  Crea un nuevo usuario con el nombre especificado.  
  - `username`: Nombre del usuario a crear.  
  - `--temp-pass`: Contraseña temporal obligatoria para el usuario.  
  - `--shell`: (Opcional) Shell por defecto, `/bin/bash` si no se especifica.  
  - `--home`: (Opcional) Directorio home del usuario.  
  - `--groups`: (Opcional) Grupos secundarios separados por comas. Ejemplo: `staff,devs`.

- `delete <username>`  
  Elimina un usuario existente.  
  - `username`: Nombre del usuario a eliminar.

- `list-users`  
  Lista todos los usuarios del sistema.

- `search-user-id <uid>`  
  Busca un usuario por su UID.  
  - `uid`: Identificador único del usuario.

---

### Gestión de Grupos

- `create-group <groupname>`  
  Crea un grupo con el nombre especificado.  
  - `groupname`: Nombre del grupo a crear.

- `create-groups <groupname1> <groupname2> ...`  
  Crea varios grupos a la vez.

- `list-groups`  
  Lista todos los grupos del sistema.

- `search-group-name <groupname>`  
  Busca un grupo por nombre.

- `modify-group <current_name> <new_name>`  
  Renombra un grupo existente.  
  - `current_name`: Nombre actual del grupo.  
  - `new_name`: Nuevo nombre para el grupo.

- `delete-group <groupname>`  
  Elimina un grupo del sistema.  
  - `groupname`: Nombre del grupo a eliminar.

---

## Uso

Ejemplo para crear un usuario:

`create alice --temp-pass "Temporal123" --shell /bin/zsh --groups staff,devs`

Ejemplo para crear varios grupos:

`create-groups devs testers,admins`

---

## Instalación y Preparación

1. Clona o descarga el repositorio y entra en la carpeta del proyecto:

   git clone <url-del-repositorio>  
   cd <nombre-de-la-carpeta>

2. Crea un entorno virtual de Python y actívalo:

   python3 -m venv venv  
   source venv/bin/activate

3. Instala las dependencias:

   pip install -r requirements.txt

4. Ante de usar la aplicación logeate con permisos de `root` usando:

   sudo -i

5. Ejecutar la aplicación:
   
   python3 app.py

---

Si tienes dudas o quieres contribuir, ¡haz un fork y abre un pull request!

---

**SysUsers** — Administración sencilla y rápida de usuarios y grupos en Linux.
