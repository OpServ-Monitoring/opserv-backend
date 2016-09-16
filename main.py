import logging
from gathering.gather_main import GatherThread
import server.__management as server
import database.dbtest as tst

from misc.logging_helper import setup_logger


LOGGINGLEVEL = logging.DEBUG

LOG_TO_FILE = True
LOG_TO_CONSOLE = True

LOG_GATHERING = True
LOG_SERVER = True


def start_gather_thread():
    print("Starting up the gathering thread.")

    gather_thread = GatherThread()
    gather_thread.daemon = True
    gather_thread.start()


def start_server():
    """
        Sets up and schedules the start of the web server
    """
    server.start()


if __name__ == '__main__':
    setup_logger(LOG_TO_CONSOLE, LOG_TO_FILE, LOGGINGLEVEL, LOG_SERVER, LOG_GATHERING)

    start_gather_thread()
    start_server()

    tst.run_me()
