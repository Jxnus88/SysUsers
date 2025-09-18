# 🧑‍💻 SysUsers - Herramienta CLI para administración de usuarios Linux

**SysUsers** es una herramienta escrita en Python diseñada para facilitar la gestión de usuarios y grupos en sistemas Linux. Ideal para **administradores de sistemas**, **DevOps**, o estudiantes que deseen automatizar tareas comunes de administración.

> 🔧 Automatiza tareas como crear usuarios, asignar grupos, configurar shells y gestionar contraseñas, todo desde una **CLI profesional**.

---

## 🚀 Funcionalidades actuales

- ✅ Crear usuarios con:
  - Home personalizado
  - Shell definido (valida shells disponibles)
  - Grupos primarios y secundarios
- ✅ Crear grupos si no existen (con confirmación interactiva)
- ✅ Validación de datos: shell válido, existencia de grupos
- ✅ CLI profesional con `argparse` y salida en colores (vía `colorama`)
- ✅ Código limpio, modular y orientado a objetos (ideal para aprender y extender)
- ✅ CLI avanzada (`sysusers.cli`)
- ✅ Gestión de roles predefinidos:
  - Añadir nuevo rol predefinido (En desarrollo)
  - Modificar rol existente (En desarrollo)
  - Ver lista de roles

---

## 💡 ¿Por qué usar SysUsers?

Aunque existen herramientas tradicionales como `adduser`, `useradd`, FreeIPA o scripts bash, **SysUsers** ofrece ventajas notables:

- ✅ Interfaz moderna, clara y enfocada en la experiencia del usuario
- ✅ Código Python fácil de entender y mantener
- ✅ Posibilidad de integrarse con CSV, logging (futuras actualizaciones), roles predefinidos y más
- ✅ Ideal para entornos educativos, profesionales o automatizados

---


## 📦 Instalación

1. Requiere Python 3.8+

2. Clona el repositorio:

    - git clone https://github.com/Jxnus88/sysusers.git
    - cd sysusers

3. Crea un entorno virtual (opcional pero recomendado):

    - python -m venv venv
    - source venv/bin/activate  # Linux/macOS

4. Instala dependencias:

    pip install -r requirements.txt

---

## ▶️ Inicio rápido

Ejecuta directamente desde dentro del proyecto con (~/sysusers):

    python3 app.py

---

## 📁 Estructura del proyecto

    sysusers/
    │
    ├── data/             
    ├── exceptions/              
    ├── handlers/            
    ├── managers/
    ├── menu/             
    ├── services/
    ├── utils/            
    ├── validators/        
    ├── __init__.py
    ├── app.py            
    ├── README.md
    ├── requirements.txt
    ├── versions_control

---

## 🔒 Permisos requeridos

Algunas funciones como la creación/eliminación de usuarios requieren privilegios de **sudo/root**.  
Asegúrate de ejecutar con permisos adecuados.

---

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia MIT** – puedes usarlo, modificarlo y distribuirlo libremente.
