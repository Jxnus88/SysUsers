import logging, getpass

def get_logger(name: str = "user_app", to_console: bool = False) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            f"%(asctime)s - [%(levelname)s] - Admin: [{getpass.getuser()}] - %(name)s: %(message)s"
        )

        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if to_console:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

    return logger
