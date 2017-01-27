"""
    Contains the description and control of argparses related to logging
    Namely consolelog and filelog
"""

from argparse import ArgumentParser, Namespace, FileType, Action
import logging
import os

from ._settings_base import SettingsBase
from misc.standalone_helper import get_path_to_app

DEFAULT_FILE_LOG_PATH = os.path.join(get_path_to_app(), "opserv.log")

class StringToLogLevel(Action):
    """
        Custom action for argparse arguments
        Maps the specified logging choices onto the correct logging level variables
    """
    def __call__(self, parser, args, values, option_string=None):
        switcher = {
            "error" : logging.ERROR,
            "warning" : logging.WARNING,
            "debug" : logging.DEBUG,
            "info" : logging.INFO,
            None : args.consolelog #Contains default value
        }
        if values in switcher:
            setattr(args, self.dest, switcher[values])
        else:
            raise ValueError("Unrecognized Logging Level")


class LoggingSettings(SettingsBase):
    """
        Inherits SettingsBase and implements functionality for applying settings onto
        the logging setup
    """
    KEY_LOG_USAGE = "log_usage"
    KEY_FILE_LOG = "filelog"
    KEY_CONSOLE_LOG = "consolelog"

    @classmethod
    def add_settings_arguments(cls, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-cl",
            "--consolelog",
            help="Enables console logging and what level should be logged",
            choices=["error", "warning", "info", "debug"],
            action=StringToLogLevel,
            nargs='?'
        )
        parser.add_argument(
            "-fl",
            "--filelog",
            help="Specified whether file logging should be enabled and where the log file will be",
            nargs="?"
        )
        parser.add_argument(
            "-usage",
            "--log_usage",
            help="Logs the usage and performance metrics of \
                     OpServ itself to identify performance issues",
            action="store_true"
        )


    @classmethod
    def validate_settings_arguments(cls, parser: ArgumentParser, args: Namespace) -> None:
        pass
