import sys
from cli import parse_args
from cli import *
from cli.menu.cli_launch_pro import launch_pro_cli
from utilis import clear_screen_cli

def main():
    if len(sys.argv) == 1:
        # sin argumentos, lanza CLI interactiva
        launch_pro_cli(dispatch_command)
    else:
        args = parse_args()
        dispatch_command(args)

def dispatch_command(args):
    # Aquí tienes que llamar la función correcta según args.command
    # Por ejemplo:
    cmd = args.command

    if cmd == "create":
        clear_screen_cli()
        create_user(args)
    elif cmd == "delete":
        clear_screen_cli()
        delete_user(args)
    elif cmd == "list-users":
        clear_screen_cli()
        list_users(args)
    elif cmd == "search-user-id":
        clear_screen_cli()
        search_user_id(args)
    elif cmd == "create-group":
        clear_screen_cli()
        create_group(args)
    elif cmd == "create-groups":
        clear_screen_cli()
        create_groups(args)
    elif cmd == "list-groups":
        clear_screen_cli()
        list_groups(args)
    elif cmd == "search-group-name":
        clear_screen_cli()
        search_group_name(args)
    elif cmd == "modify-group":
        clear_screen_cli()
        modify_group(args)
    elif cmd == "delete-group":
        clear_screen_cli()
        delete_group(args)
    else:
        print("Comando no reconocido.")

if __name__ == "__main__":
    main()
