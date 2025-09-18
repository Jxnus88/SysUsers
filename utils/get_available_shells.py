

def get_available_shells():
    try:
        with open("/etc/shells", "r") as f:
            shells = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return shells
    except FileExistsError:
        return ["/bin/bash", "/bin/sh"]