import unittest
from unittest.mock import patch
import subprocess
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from manager.user_manager import UserManager
from exceptions import (
    InvalidShellError,
    UserAlreadyExists,
    UserCreationError,
    PathHomeError,
    InvalidHomeError,
    NotExistGroupError,
    # Asumo que importas NotPasswdError también
    NotPasswdError
)
from loggin.logger import get_logger

logger = get_logger(name="test_user_manager", to_console=True)


class TestUserManager(unittest.TestCase):

    def setUp(self):
        logger.info("Setup UserManager instance")
        self.um = UserManager()

        # Mock validadores para que no fallen (a menos que se defina side_effect)
        patcher_user = patch.object(self.um.user_validate, "validate_user_not_exists")
        self.mock_validate_user = patcher_user.start()
        self.addCleanup(patcher_user.stop)
        self.mock_validate_user.return_value = None

        patcher_shell = patch.object(self.um.shell_validate, "validate_shell")
        self.mock_shell_validate = patcher_shell.start()
        self.addCleanup(patcher_shell.stop)
        self.mock_shell_validate.return_value = None

        patcher_home = patch.object(self.um.home_validate, "validate_home")
        self.mock_home_validate = patcher_home.start()
        self.addCleanup(patcher_home.stop)
        self.mock_home_validate.return_value = None

        patcher_group = patch.object(self.um.group_validate, "validate_group")
        self.mock_group_validate = patcher_group.start()
        self.addCleanup(patcher_group.stop)
        self.mock_group_validate.return_value = None

        patcher_passwd = patch.object(self.um.passwd_validate, "validate_passwd")
        self.mock_passwd_validate = patcher_passwd.start()
        self.addCleanup(patcher_passwd.stop)
        self.mock_passwd_validate.return_value = None


    @patch("manager.user_manager.subprocess.run")
    def test_create_user_successfully(self, mock_subproc_run):
        logger.info("Test: test_create_user_successfully started")
        mock_subproc_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)

        try:
            self.um.create_user(
                username="juan",
                home="/home/juan",
                shell="/bin/bash",
                list_groups=["users"],
                temp_pass="123456"
            )
            logger.info("Usuario creado correctamente en test_create_user_successfully")
        except Exception as e:
            self.fail(f"Fallo inesperado al crear usuario: {e}")

        logger.info("Test: test_create_user_successfully terminado con éxito")


    def test_invalid_home_path(self):
        logger.info("Test: test_invalid_home_path iniciado")
        self.mock_home_validate.side_effect = PathHomeError("Home no válido")

        with self.assertRaises(PathHomeError):
            self.um.create_user(
                username="juan",
                home="relative/path/home",  # No es ruta absoluta
                shell="/bin/bash",
                temp_pass="123456"
            )
        logger.info("Test: test_invalid_home_path terminado correctamente")


    def test_invalid_shell(self):
        logger.info("Test: test_invalid_shell iniciado")
        self.mock_shell_validate.side_effect = InvalidShellError("Shell no válida")

        with self.assertRaises(InvalidShellError):
            self.um.create_user(
                username="juan",
                home="/home/juan",
                shell="/bin/fake_shell",
                temp_pass="123456"
            )
        logger.info("Test: test_invalid_shell terminado correctamente")


    def test_password_not_provided(self):
        logger.info("Test: test_password_not_provided iniciado")
        self.mock_passwd_validate.side_effect = NotPasswdError("Contraseña no proporcionada")

        with self.assertRaises(NotPasswdError):
            self.um.create_user(
                username="juan",
                home="/home/juan",
                shell="/bin/bash",
                temp_pass=""  # Contraseña vacía, invalida
            )
        logger.info("Test: test_password_not_provided terminado correctamente")


    @patch("manager.user_manager.subprocess.run")
    def test_subprocess_failure(self, mock_subproc_run):
        logger.info("Test: test_subprocess_failure iniciado")
        mock_subproc_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd=['useradd'])

        with self.assertRaises(UserCreationError) as context:
            self.um.create_user(
                username="juan",
                home="/home/juan",
                shell="/bin/bash",
                temp_pass="123456"
            )

        self.assertIn("No se pudo crear el usuario", str(context.exception))
        logger.info("Test: test_subprocess_failure terminado correctamente")


if __name__ == "__main__":
    logger.info("Iniciando suite de tests")
    unittest.main()
    logger.info("Suite de tests finalizada")
