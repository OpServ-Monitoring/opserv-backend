import logging
import sys

from application_settings.logging_settings import LoggingSettings


def setup_argparse_logger():
    # TODO Use LoggingSettings.get_setting(LoggingSettings.KEY_LOG_LEVEL)
    # TODO Transform to  logging  package values
    logging_level = logging.DEBUG

    setup_logger(
        LoggingSettings.get_setting(LoggingSettings.KEY_LOG_TO_CONSOLE),
        LoggingSettings.get_setting(LoggingSettings.KEY_LOG_TO_FILE),
        logging_level,
        True,
        True
    )


def setup_logger(log_to_console, log_to_file, logging_level, log_server, log_gathering):
    # SETUP LOGGER
    mainLog = logging.getLogger("opserv")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create file handler, set the formatting to it and add it as an handler
    if log_to_file:
        # TODO Use runtime arg - maybe as a param to prevent dependencies
        # logging_file = LoggingSettings.get_setting(LoggingSettings.KEY_LOGGING_FILE)

        fh = logging.FileHandler('opserv.log')
        fh.setLevel(logging_level)
        fh.setFormatter(formatter)
        mainLog.addHandler(fh)

    # Create Console logging handler, if activated
    if log_to_console:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging_level)
        # create formatter and add it to the handlers
        ch.setFormatter(formatter)

        # Add the desired filters to the console handler
        if not log_gathering:
            ch.addFilter(Blacklist("opserv.gathering"))
        if not log_server:
            ch.addFilter(Blacklist("osperv.server"))
        # add the handler to the logger
        mainLog.addHandler(ch)


class Whitelist(logging.Filter):
    """ src: http://stackoverflow.com/questions/17275334/what-is-a-correct-way-to-filter-different-loggers-using-python-logging """

    def __init__(self, *whitelist):
        self.whitelist = [logging.Filter(name) for name in whitelist]

    def filter(self, record):
        return any(f.filter(record) for f in self.whitelist)


class Blacklist(Whitelist):
    """ src: http://stackoverflow.com/questions/17275334/what-is-a-correct-way-to-filter-different-loggers-using-python-logging """

    def filter(self, record):
        return not Whitelist.filter(self, record)
