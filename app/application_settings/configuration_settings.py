import json
from argparse import ArgumentParser, Namespace
from os.path import isfile, join

from misc.helper import get_path_to_app, is_pathname_valid
from ._settings_base import SettingsBase

DEFAULT_CONFIG_FILE = join(get_path_to_app(), "opserv_config.json")


class ConfigurationSettings(SettingsBase):
    KEY_CONF_FILE = "conffile"

    @classmethod
    def add_settings_arguments(cls, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-cf",
            "--conffile",
            help="The path to a configuration file to read args from. Runtime args override these."
                 "Must be a valid JSON object",
            default=DEFAULT_CONFIG_FILE
        )

    @classmethod
    def validate_settings_arguments(cls, parser: ArgumentParser, args: Namespace) -> None:
        if "conf_file" in args and args.conf_file is not None:
            if not is_pathname_valid(args.conf_file):
                parser.error("Pathname is not valid {}".format(args.conf_file.name))

    @classmethod
    def config_is_missing(cls):
        if isfile(cls.get_setting(cls.KEY_CONF_FILE)):
            return False
        return True

    @classmethod
    def create_empty_config(cls):
        file_handle = open(cls.get_setting(cls.KEY_CONF_FILE), "w")
        file_handle.write("{}")
        file_handle.close()

    @classmethod
    def config_file_is_valid(cls):
        # Does not account for writing permission validity
        try:
            conf_file = json.load(open(cls.get_setting(cls.KEY_CONF_FILE), "r"))
            if isinstance(conf_file, dict):
                return True
            return False
        except ValueError:
            return False
        except TypeError:
            return False
        except FileNotFoundError:
            return False

    @classmethod
    def get_config_as_dict(cls):
        return json.load(open(cls.get_setting(cls.KEY_CONF_FILE), "r"))
