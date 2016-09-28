#
# Main system launch file, creates the gathering thread and starts flask
#
# 27.09.2016
#
# Usage: Simply launch this file
#


import logging

import database.dbtest as tst
import server.__management as server
from gathering.gather_main import GatherThread
from misc.logging_helper import setup_logger

LOGGINGLEVEL = logging.DEBUG

LOG_TO_FILE = False
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
