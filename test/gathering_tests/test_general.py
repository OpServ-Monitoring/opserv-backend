#
# Test Script for the gathering side of the project that will test all the gathering methods
#
# 27.09.2016
#
# Usage: Simply launch this python script
#

import logging
from contextlib import contextmanager

from database.unified_database_interface import UnifiedDatabaseInterface
from gathering.gather_main import GatherThread

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
    UnifiedDatabaseInterface.get_database_opener().create_database()
    return
