import argparse

from . import _settings_base as application_settings_store
from .logging_settings import LoggingSettings
from .server_settings import ServerSettings


def init():
    # Set up a argsparse.ArgumentParser
    parser = configure_runtime_arg_parser()

    # Validate the parsed runtime args
    runtime_args = validate_runtime_args(parser)

    # TODO Read arguments from file if set

    # Globally save the runtime args
    application_settings_store.settings = vars(runtime_args)


def configure_runtime_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    # ConfigurationSettings.add_settings_arguments(parser)
    LoggingSettings.add_settings_arguments(parser)
    ServerSettings.add_settings_arguments(parser)

    return parser


def validate_runtime_args(parser) -> argparse.Namespace:
    args = parser.parse_args()

    # ConfigurationSettings.validate_settings_arguments(parser, args)
    LoggingSettings.validate_settings_arguments(parser, args)
    ServerSettings.validate_settings_arguments(parser, args)

    return args
