import argparse

class ArgumentParserNoExit(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        # En vez de salir, solo lanzamos una excepción para que puedas manejarlo
        if message:
            print(message)
        raise Exception("HelpShown")

    def error(self, message):
        # En vez de llamar a exit, mostramos el error y lanzamos excepción
        self.print_usage()
        print(f"Error: {message}")
        raise Exception("ArgumentError")
