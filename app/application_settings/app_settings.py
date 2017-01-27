"""
    Adds the AppSettings SettingsBase that contains argument parsing
    for the main application
"""
from argparse import ArgumentParser, Namespace

from ._settings_base import SettingsBase


class AppSettings(SettingsBase):
    """
        Adds and validated the arguments for the main application
        Currently only adds skipping arguments for the startup sequence
    """
    KEY_SKIP_CONFIG = "skipconfig"
    KEY_PASSWORD = "password"

    @classmethod
    def add_settings_arguments(cls, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-skipc",
            "--skipconfig",
            help="Skips the configuration setup and uses default values",
            action="store_true"
        )

        parser.add_argument(
            "-pw",
            "--password",
            help="Simple password to have atleast some protection against unwanted clients"
        )

    @classmethod
    def validate_settings_arguments(cls, parser: ArgumentParser, args: Namespace) -> None:
        pass
