import argparse
import json

from . import _settings_base as application_settings_store
from .logging_settings import LoggingSettings
from .server_settings import ServerSettings
from .configuration_settings import ConfigurationSettings


# TODO Fix this! - as of now as everything defaults to None file args will not affect the settings
def init():
    # Set up a argsparse.ArgumentParser
    parser = configure_runtime_arg_parser()

    # Validate the passed runtime args
    console_args = validate_runtime_args(parser)
    console_args_as_dict = vars(console_args)

    # Read arguments passed in a file
    file_args = {}
    if console_args_as_dict["conf_file"] is not None:
        file_args = json.loads(
            console_args.conf_file.read()
        )

    # Globally save the runtime args
    application_settings_store.settings = file_args.copy()
    application_settings_store.settings.update(console_args_as_dict)


def configure_runtime_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    ConfigurationSettings.add_settings_arguments(parser)
    LoggingSettings.add_settings_arguments(parser)
    ServerSettings.add_settings_arguments(parser)

    return parser


def validate_runtime_args(parser) -> argparse.Namespace:
    args = parser.parse_args()

    ConfigurationSettings.validate_settings_arguments(parser, args)
    LoggingSettings.validate_settings_arguments(parser, args)
    ServerSettings.validate_settings_arguments(parser, args)

    return args
