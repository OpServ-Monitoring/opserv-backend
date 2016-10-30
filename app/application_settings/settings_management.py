import argparse

runtime_settings = None


def init():
    global runtime_settings
    runtime_settings = {}

    __parse_runtime_args()


def __parse_runtime_args():
    parser = argparse.ArgumentParser()

    __configure_configuration_args(parser)
    __configure_encryption_args(parser)
    __configure_authentication_args(parser)

    args = parser.parse_args()

    __parse_configuration_args(parser, args)


def __configure_configuration_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-cf",
        "--conf-file",
        help="The path to a configuration file to read args from. Runtime args override these."
             "Must be a valid JSON object",
        type=argparse.FileType('r')
    )

    __configure_conf_logging_args(parser)

    parser.add_argument(
        "-p",
        "--port",
        help="Configure the port the server should run on.",
        type=int
        # choices=list(range(0, 65536))
    )


def __configure_conf_logging_args(parser: argparse.ArgumentParser):
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
        type=argparse.FileType('w')
    )


def __parse_configuration_args(parser, args):
    # Check configuration file and save args
    pass

    # Check logging args
    runtime_settings["log-to-console"] = args.log_to_console
    runtime_settings["log-to-file"] = args.log_to_file

    if runtime_settings["log-to-file"] and args.logging_file is None:
        parser.error("-logtf, --log-to-file requires -logf")
    else:
        runtime_settings["log-file-path"] = args.logging_file

    # Save port to settings
    if args.port is not None:
        runtime_settings["port"] = args.port


def __configure_encryption_args(parser: argparse.ArgumentParser):
    pass


def __configure_authentication_args(parser: argparse.ArgumentParser):
    pass


"""
Upcoming

SECURITY

cert    tls-cert
OR
certf   tls-cert-path

key     tls-key
OR
keyf    tls-key-path

e       encrypt         default false


AUTHENTICATION
See GitHub issue https://github.com/OpServ-Monitoring/opserv-backend/issues/16
"""
