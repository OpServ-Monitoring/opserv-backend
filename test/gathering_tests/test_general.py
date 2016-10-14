#
# Test Script for the gathering side of the project that will test all the gathering methods
#
# 27.09.2016
#
# Usage: Simply launch this python script
#

import logging
import threading
import time
from contextlib import contextmanager


import misc.queue_manager as queue_manager
import misc.data_manager as data_manager
from gathering.gather_main import GatherThread
from misc.logging_helper import setup_logger
from misc.constants import implemented_hardware, HARDWARE_DEFAULTS
from database.database_open_helper import DatabaseOpenHelper


log = logging.getLogger("opserv.test")
log.setLevel(logging.DEBUG)

@contextmanager
def start_gather_thread():
    log.debug("Starting up the gathering thread.")

    gather_thread = GatherThread()
    gather_thread.daemon = True
    gather_thread.start()
    yield gather_thread
    gather_thread.running = False

def mock_db_open():
    DatabaseOpenHelper.mock_on_create()
    return
