"""
 Main system launch file, creates the gathering thread and starts flask

 27.09.2016

 Usage: Simply launch this file
"""

import application_settings.settings_management as app_settings
import misc.data_manager as data_manager
import misc.queue_manager as queue_manager
import server.__management as server
from database.unified_database_interface import UnifiedDatabaseInterface
from gathering.gather_main import GatherThread
from misc.logging_helper import setup_argparse_logger


def init_database():
    """
        Initiates the database
    """
    UnifiedDatabaseInterface.get_database_opener().create_database()
    UnifiedDatabaseInterface.get_database_opener().set_gathering_rates()


def start_gather_thread():
    """
        Starts the gathering thread as a daemon
    """
    print("Starting up the gathering thread.")  # TODO Exchange with logging

    gather_thread = GatherThread()
    gather_thread.daemon = True
    gather_thread.start()


def start_server():
    """
        Sets up and schedules the start of the web server
    """
    server.start()


def manage_runtime_settings():
    # TODO Document this function
    app_settings.init()


if __name__ == '__main__':
    manage_runtime_settings()

    setup_argparse_logger()

    queue_manager.init()
    data_manager.init()

    init_database()

    start_gather_thread()
    start_server()
