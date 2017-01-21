import argparse

from . import _settings_base as application_settings_store
from .app_settings import AppSettings
from .configuration_settings import ConfigurationSettings
from .logging_settings import LoggingSettings
from .server_settings import ServerSettings


# TODO Fix this! - as of now as everything defaults to None file args will not affect the settings
def init():
    # Set up a argsparse.ArgumentParser
    parser = configure_runtime_arg_parser()

    # Validate the passed runtime args
    console_args = validate_runtime_args(parser)
    console_args_as_dict = vars(console_args)

    application_settings_store.settings = console_args_as_dict

    # Now validate the integrity of the config file
    config_file_path = ConfigurationSettings.get_setting(ConfigurationSettings.KEY_CONF_FILE)
    if ConfigurationSettings.config_is_missing():
        # If there is no config file, create a new one
        ConfigurationSettings.create_empty_config()

    if not ConfigurationSettings.config_file_is_valid():
        raise ValueError("Configuration file is invalid")

    # Load the config file into runtime
    config_dict = ConfigurationSettings.get_config_as_dict()

    # Globally save the runtime args
    application_settings_store.settings = config_dict
    for arg in console_args_as_dict:
        if arg in application_settings_store.settings:
            if console_args_as_dict[arg] is not None:
                application_settings_store.settings[arg] = console_args_as_dict[arg]
        else:
            application_settings_store.settings[arg] = console_args_as_dict[arg]


def configure_runtime_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    ConfigurationSettings.add_settings_arguments(parser)
    LoggingSettings.add_settings_arguments(parser)
    ServerSettings.add_settings_arguments(parser)
    AppSettings.add_settings_arguments(parser)

    return parser


def validate_runtime_args(parser) -> argparse.Namespace:
    args = parser.parse_args()

    ConfigurationSettings.validate_settings_arguments(parser, args)
    LoggingSettings.validate_settings_arguments(parser, args)
    ServerSettings.validate_settings_arguments(parser, args)
    AppSettings.validate_settings_arguments(parser, args)

    return args
