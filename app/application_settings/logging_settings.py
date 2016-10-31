from argparse import ArgumentParser, Namespace, FileType

from ._settings_base import SettingsBase


class LoggingSettings(SettingsBase):
    KEY_LOG_TO_CONSOLE = "log_to_console"
    KEY_LOG_TO_FILE = "log_to_file"
    KEY_LOG_LEVEL = "log_level"
    KEY_LOGGING_FILE = "logging_file"

    @classmethod
    def add_settings_arguments(cls, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-logtc",
            "--log-to-console",
            help="Outputs the log on the python console. Defaults to false",
            action="store_true",
            default=False
        )

        parser.add_argument(
            "-logtf",
            "--log-to-file",
            help="Outputs the log into the file at the specified path. Defaults to false",
            action="store_true",
            default=False
        )

        parser.add_argument(
            "-logl",
            "--log-level",
            help="Specify the level of messages to log, higher levels included. Defaults to error level.",
            choices=["none", "error", "warning", "info", "debug"],
            default="error"
        )

        parser.add_argument(
            "-logf",
            "--logging-file",
            help="The path to the file the log should be written to",
            type=FileType('w')
        )

    @classmethod
    def validate_settings_arguments(cls, parser: ArgumentParser, args: Namespace) -> None:
        if args.log_to_file and args.logging_file is None:
            parser.error("-logtf, --log-to-file requires -logf")
