"""
 Main system launch file, creates the gathering thread and starts flask

 27.09.2016

 Usage: Simply launch this file
"""

import logging

import server.__management as server
from gathering.gather_main import GatherThread
from misc.logging_helper import setup_logger
import misc.data_manager as data_manager
import misc.queue_manager as queue_manager

from database.database_open_helper import DatabaseOpenHelper

LOGGINGLEVEL = logging.DEBUG

LOG_TO_FILE = False
LOG_TO_CONSOLE = True

LOG_GATHERING = True
LOG_SERVER = True


def init_database():
    """
        Initiates the database
    """
    DatabaseOpenHelper().on_create()


def start_gather_thread():
    """
        Starts the gathering thread as a daemon
    """
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
    queue_manager.init()
    data_manager.init()
    init_database()

    start_gather_thread()
    start_server()
