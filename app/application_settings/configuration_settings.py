import json
from argparse import ArgumentParser, Namespace, FileType

from ._settings_base import SettingsBase


class ConfigurationSettings(SettingsBase):
    @classmethod
    def add_settings_arguments(cls, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-cf",
            "--conf-file",
            help="The path to a configuration file to read args from. Runtime args override these."
                 "Must be a valid JSON object",
            type=FileType('r')
        )

    @classmethod
    def validate_settings_arguments(cls, parser: ArgumentParser, args: Namespace) -> None:
        if "conf_file" in args and args.conf_file is not None:
            try:
                json.load(
                    open(args.conf_file, "r")
                )
            except json.JSONDecodeError:
                parser.error("-cf, --conf-file has to be a valid json object")
