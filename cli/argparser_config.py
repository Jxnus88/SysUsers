from argparse import ArgumentParser
from cli import (
    create_user, delete_user, list_users, search_user_id,
    create_group, create_groups, list_groups,
    search_group_name, modify_group, delete_group
)
from exceptions import ArgumentParserNoExit

def parse_args(argv=None):
    parser = ArgumentParserNoExit(
        description="SysUsers - Administrador de usuarios para Linux"
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # ------------------- USUARIOS -------------------
    create_parser = subparsers.add_parser("create", help="Crear un nuevo usuario.")
    create_parser.add_argument("username", help="Nombre del usuario.")
    create_parser.add_argument("--shell", default="/bin/bash", help="Shell del usuario.")
    create_parser.add_argument("--home", help="Directorio home.")
    create_parser.add_argument(
        "--groups",
        help="Grupos secundarios separados por comas. Ejemplo: 'staff,devs'"
    )
    create_parser.add_argument("--temp-pass", required=True, help="Contraseña temporal.")
    create_parser.set_defaults(func=create_user)

    delete_parser = subparsers.add_parser("delete", help="Eliminar un usuario.")
    delete_parser.add_argument("username", help="Nombre del usuario.")
    delete_parser.set_defaults(func=delete_user)

    list_users_parser = subparsers.add_parser("list-users", help="Listar usuarios.")
    list_users_parser.set_defaults(func=list_users)

    search_uid_parser = subparsers.add_parser("search-user-id", help="Buscar usuario por UID.")
    search_uid_parser.add_argument("uid", type=int, help="UID a buscar.")
    search_uid_parser.set_defaults(func=search_user_id)

    # ------------------- GRUPOS -------------------
    group_create_parser = subparsers.add_parser("create-group", help="Crear un grupo.")
    group_create_parser.add_argument("groupname", help="Nombre del grupo.")
    group_create_parser.set_defaults(func=create_group)

    groups_create_parser = subparsers.add_parser("create-groups", help="Crear varios grupos.")
    groups_create_parser.add_argument("groupnames", nargs="+", help="Nombres de los grupos.")
    groups_create_parser.set_defaults(func=create_groups)

    list_groups_parser = subparsers.add_parser("list-groups", help="Listar grupos.")
    list_groups_parser.set_defaults(func=list_groups)

    search_group_parser = subparsers.add_parser("search-group-name", help="Buscar grupo.")
    search_group_parser.add_argument("groupname", help="Nombre del grupo.")
    search_group_parser.set_defaults(func=search_group_name)

    modify_group_parser = subparsers.add_parser("modify-group", help="Renombrar grupo.")
    modify_group_parser.add_argument("current_name", help="Nombre actual.")
    modify_group_parser.add_argument("new_name", help="Nuevo nombre.")
    modify_group_parser.set_defaults(func=modify_group)

    delete_group_parser = subparsers.add_parser("delete-group", help="Eliminar grupo.")
    delete_group_parser.add_argument("groupname", help="Nombre del grupo.")
    delete_group_parser.set_defaults(func=delete_group)

    return parser.parse_args(argv)
