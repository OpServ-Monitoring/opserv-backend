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

import queue_manager
from gathering.gather_main import GatherThread
from misc.logging_helper import setup_logger
from misc.constants import implemented_hardware, HARDWARE_DEFAULTS


LOGGINGLEVEL = logging.DEBUG

LOG_TO_FILE = False
LOG_TO_CONSOLE = True

LOG_GATHERING = True
LOG_SERVER = True

DATA_TEST_TIMEOUT = 2.5
MAX_TEST_ITERATIONS = 10

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
    queue_manager.setGatheringRateQueue.put({"hardware": "cpu", "valueType": "load", "delayms": 1000})
    queue_manager.setGatheringRateQueue.put({"hardware": "memory", "valueType": "used", "delayms": 1000})
    queue_manager.setGatheringRateQueue.put({"hardware": "cpu", "valueType": "cores", "delayms": 5000})
    queue_manager.setGatheringRateQueue.put({"hardware": "cpu", "valueType": "cores", "delayms": 0})


def testInsertSystemGathering():
    # One Time Test
    log.info("One Shot System Gathering")
    queue_manager.requestDataQueue.put({"hardware": "system", "valueType": "cpus"})
    queue_manager.requestDataQueue.put({"hardware": "system", "valueType": "gpus"})
    queue_manager.requestDataQueue.put({"hardware": "system", "valueType": "disks"})
    queue_manager.requestDataQueue.put({"hardware": "system", "valueType": "cores"})
    queue_manager.requestDataQueue.put({"hardware": "system", "valueType": "processes"})
    queue_manager.requestDataQueue.put({"hardware": "system", "valueType": "networks"})


    # Gathering Rate Test
    log.info("Adding System Gathering")
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "cpus", "delayms": 1000})
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "gpus", "delayms": 1000})
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "disks", "delayms": 1000})
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "cores", "delayms": 1000})
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "processes", "delayms": 1000})
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "networks", "delayms": 1000})

    time.sleep(2)
    log.info("Removing System Gathering")
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "cpus", "delayms": 0})
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "gpus", "delayms": 0})
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "disks", "delayms": 0})
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "cores", "delayms": 0})
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "processes", "delayms": 0})
    queue_manager.setGatheringRateQueue.put({"hardware": "system", "valueType": "networks", "delayms": 0})

def testAllHardware():
    # For each hardware in the hardware list
    for hw in implemented_hardware:
        # For Each valueType of that specific hardware
        log.info("Testing {}".format(implemented_hardware[hw]))
        for vT in implemented_hardware[hw]:
            if HARDWARE_DEFAULTS[hw][0] and HARDWARE_DEFAULTS[hw][1] != None:
                queue_manager.requestDataQueue.put({"hardware": hw, "valueType": vT, "args" : HARDWARE_DEFAULTS[hw][1]})
                queue_manager.getQueue(hw,vT,HARDWARE_DEFAULTS[hw][1]).get(timeout=DATA_TEST_TIMEOUT)
            elif not HARDWARE_DEFAULTS[hw][0]:
                queue_manager.requestDataQueue.put({"hardware": hw, "valueType": vT})
                queue_manager.getQueue(hw,vT).get(timeout=DATA_TEST_TIMEOUT)

class TestThread(threading.Thread):
    def __init__(self):
        """
            Main Init function for the test thread
        """
        log.debug("Initializing TestThread...")
        threading.Thread.__init__(self)
        return

    def run(self):
        startTimeTest = time.time()
        insertTestDataIntoQueue()
        testInsertSystemGathering()
        testAllHardware()
        currentIterations = 0
        startTimeIterations = time.time()
        while currentIterations < MAX_TEST_ITERATIONS:
            while not queue_manager.getQueue("cpu", 0, "load").empty():
                log.debug(queue_manager.getQueue("cpu", 0, "load").get(False))

            while not queue_manager.getQueue("cpu", "load", 0).empty():
                log.debug(queue_manager.getQueue("cpu", "load", 0).get(False))
            while not queue_manager.getQueue("memory", "used").empty():
                log.debug(queue_manager.getQueue("memory", "used").get(False))
            currentIterations += 1
            time.sleep(0.5)
            log.debug(currentIterations)
            log.debug("Tick")
        endTime = time.time()
        log.info("Completed Test with {0} iterations over {1} seconds".format(currentIterations, endTime - startTimeIterations ))
        log.info("Whole test finished in {} seconds".format(endTime - startTimeTest))
if __name__ == '__main__':
    setup_logger(LOG_TO_CONSOLE, LOG_TO_FILE, LOGGINGLEVEL, LOG_SERVER, LOG_GATHERING)
    start_gather_thread()
    start_test_thread()
    while True:
        time.sleep(5)
