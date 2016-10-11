import logging
import appendApp

from misc.logging_helper import setup_logger
import misc.data_manager as data_manager
import misc.queue_manager as queue_manager

LOGGINGLEVEL = logging.DEBUG

LOG_TO_FILE = False
LOG_TO_CONSOLE = True

LOG_GATHERING = True
LOG_SERVER = True

def pytest_configure():
    print("PyTest conftest was loaded")
    setup_logger(LOG_TO_CONSOLE, LOG_TO_FILE, LOGGINGLEVEL, LOG_SERVER, LOG_GATHERING)
    print("Logger Started")

def pytest_runtest_setup():
    # Ensure tests are run in fresh environments
    queue_manager.init()
    data_manager.init()