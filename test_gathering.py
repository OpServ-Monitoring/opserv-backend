import time
import threading

from gathering.gather_main import GatherThread
import queue_manager
from misc.logging_helper import setup_logger
import logging

LOGGINGLEVEL = logging.DEBUG

LOG_TO_FILE = True
LOG_TO_CONSOLE = True

LOG_GATHERING = False
LOG_SERVER = True


log = logging.getLogger("opserv.gatheringTest")
log.setLevel(logging.DEBUG)

def start_gather_thread():
    log.debug("Starting up the gathering thread.")

    gather_thread = GatherThread()
    gather_thread.daemon = True
    gather_thread.start()


def start_test_thread():
    log.debug("Starting Test Thread")
    test_thread = TestThread()
    test_thread.daemon = True
    test_thread.start()


def insertTestDataIntoQueue():
    """
        Inserts testing data into the gatheringrate and request queues
    """
    queue_manager.setGatheringRateQueue.put({"hardware" : "cpu", "valueType" : "load", "delayms" : 1000})
    queue_manager.setGatheringRateQueue.put({"hardware" : "memory", "valueType" : "used", "delayms" : 1000})
    queue_manager.setGatheringRateQueue.put({"hardware" : "cpu", "valueType" : "cores", "delayms" : 5000})
    queue_manager.requestDataQueue.put({"hardware" : "disk", "valueType" : "partitions", "args" : "all"})
    queue_manager.requestDataQueue.put({"hardware" : "process", "valueType" : "getall"})
    queue_manager.setGatheringRateQueue.put({"hardware" : "cpu", "valueType" : "cores", "delayms" : 0})


class TestThread(threading.Thread):
    def __init__(self):
        """
            Main Init function for the test thread
        """
        log.debug("Initializing TestThread...")
        threading.Thread.__init__(self)
        return

    def run(self):
        insertTestDataIntoQueue()
        while True:
            while not queue_manager.getQueue("cpu", 0, "load").empty():
                log.debug(queue_manager.getQueue("cpu",0, "load").get(False))

            while not queue_manager.getQueue("cpu", "load", 0).empty():
                log.debug(queue_manager.getQueue("cpu","load", 0).get(False))
            while not queue_manager.getQueue("memory", "used").empty():
                log.debug(queue_manager.getQueue("memory","used").get(False))
                
            time.sleep(0.5)


if __name__ == '__main__':
    setup_logger(LOG_TO_CONSOLE, LOG_TO_FILE, LOGGINGLEVEL, LOG_SERVER, LOG_GATHERING)
    start_gather_thread()
    start_test_thread()
    while True:
        time.sleep(5)