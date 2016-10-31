from argparse import ArgumentParser, Namespace

from ._settings_base import SettingsBase


class ServerSettings(SettingsBase):
    KEY_PORT = "port"

    @classmethod
    def add_settings_arguments(cls, parser: ArgumentParser) -> None:
        cls.__add_general_arguments(parser)
        cls.__add_encryption_arguments(parser)
        cls.__add_authentication_arguments(parser)

    @classmethod
    def __add_general_arguments(cls, parser: ArgumentParser):
        parser.add_argument(
            "-p",
            "--port",
            help="Configure the port the server should run on.",
            type=int
        )

    @classmethod
    def __add_encryption_arguments(cls, parser: ArgumentParser):
        # TODO Add encryption arguments
        # see https://github.com/OpServ-Monitoring/opserv-backend/issues/16

        pass

    @classmethod
    def __add_authentication_arguments(cls, parser: ArgumentParser):
        # TODO Add authentication arguments
        # see https://github.com/OpServ-Monitoring/opserv-backend/issues/16

        pass

    @classmethod
    def validate_settings_arguments(cls, parser: ArgumentParser, args: Namespace) -> None:
        if "port" in args:
            port = args.port

            if port is not None and (port < 0 or port > 65535):
                parser.error("-p, --port has to define a port number between 0 and 65535")
