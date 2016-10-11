import logging
import appendApp

from misc.logging_helper import setup_logger


LOGGINGLEVEL = logging.DEBUG

LOG_TO_FILE = False
LOG_TO_CONSOLE = True

LOG_GATHERING = True
LOG_SERVER = True

def pytest_configure():
    print("PyTest conftest was loaded")
    setup_logger(LOG_TO_CONSOLE, LOG_TO_FILE, LOGGINGLEVEL, LOG_SERVER, LOG_GATHERING)
    print("Logger Started")