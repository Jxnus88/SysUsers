import argparse

class ArgumentParserNoExit(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if message:
            print(message)
        raise Exception("Fin del comando (pero sin salir del programa).")

    def error(self, message):
        self.print_help()
        raise Exception(f"[ArgParse] Error: {message}")