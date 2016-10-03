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

import misc.queue_manager as queue_manager
import misc.data_manager as data_manager
from gathering.gather_main import GatherThread
from misc.logging_helper import setup_logger
from misc.constants import implemented_hardware, HARDWARE_DEFAULTS
from database.database_open_helper import DatabaseOpenHelper


LOGGINGLEVEL = logging.DEBUG

LOG_TO_FILE = False
LOG_TO_CONSOLE = True

LOG_GATHERING = True
LOG_SERVER = True

DATA_TEST_TIMEOUT = 2.5
MAX_TEST_ITERATIONS = 10
ITERATION_TEST_SPEED = 500
DATA_MANAGER_TIMEOUT = 5
DATA_MANAGER_TEST_COMPONENT = "cpu"
DATA_MANAGER_TEST_METRIC = "usage"

log = logging.getLogger("opserv.gatheringTest")
log.setLevel(logging.DEBUG)


def start_gather_thread():
    log.debug("Starting up the gathering thread.")

    gather_thread = GatherThread()
    gather_thread.daemon = True
    gather_thread.start()
    return gather_thread


def start_test_thread():
    log.debug("Starting Test Thread")
    test_thread = TestThread()
    test_thread.daemon = True
    test_thread.start()
    return test_thread

def insertTestDataIntoQueue():
    """
        Inserts testing data into the gatheringrate and request queues
    """
    queue_manager.setGatheringRate("cpu", "usage", 1000)
    queue_manager.setGatheringRate("memory", "used", 1000)


def testInsertSystemGathering():
    # One Time Test
    log.info("One Shot System Gathering") 
    queue_manager.requestData("system", "cpus")
    queue_manager.requestData("system", "gpus")
    queue_manager.requestData("system", "disks")
    queue_manager.requestData("system", "cores")
    queue_manager.requestData("system", "processes")
    queue_manager.requestData("system", "networks")


    # Gathering Rate Test
    log.info("Adding System Gathering")
    queue_manager.setGatheringRate("system","cpus", 1000)
    queue_manager.setGatheringRate("system","gpus", 1000)
    queue_manager.setGatheringRate("system","disks", 1000)
    queue_manager.setGatheringRate("system","cores", 1000)
    queue_manager.setGatheringRate("system","processes", 1000)
    queue_manager.setGatheringRate("system","networks", 1000)

    time.sleep(2)
    log.info("Removing System Gathering")
    queue_manager.setGatheringRate("system","cpus", 0)
    queue_manager.setGatheringRate("system","gpus", 0)
    queue_manager.setGatheringRate("system","disks", 0)
    queue_manager.setGatheringRate("system","cores", 0)
    queue_manager.setGatheringRate("system","processes", 0)
    queue_manager.setGatheringRate("system","networks", 0)

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

def testRateSpeed(iterations, speed):
    # Start rate update with specifc speed
    queue_manager.setGatheringRate("cpu", "usage", speed)

    currentIterations = 0
    # Wait while data arrives
    while currentIterations < iterations:
        # Calc mS to seconds and add half a second timeout buffer
        if not queue_manager.getQueue("cpu", "usage").empty():
            queue_manager.getQueue("cpu", "usage").get(timeout=(speed / 1000) + 0.5)        
            currentIterations += 1
        time.sleep(speed / 10000)
    return

def testDataManager():
    log.info("Starting Data Manager Test")

    # Disable any gathering rates for the tested component to avoid any wrong results
    queue_manager.setGatheringRate(DATA_MANAGER_TEST_COMPONENT, DATA_MANAGER_TEST_METRIC, 0)

    # Save the current value in the realtime data dictionary
    startData = data_manager.getMeasurement(DATA_MANAGER_TEST_COMPONENT, DATA_MANAGER_TEST_METRIC)

    # Ask for a data update
    queue_manager.requestData(DATA_MANAGER_TEST_COMPONENT, DATA_MANAGER_TEST_METRIC)
    startTime = time.time()
    dataIsTheSame = True

    # Wait till the new one arrives or timeout expires
    while time.time() - startTime < DATA_MANAGER_TIMEOUT and dataIsTheSame:
        newData = data_manager.getMeasurement(DATA_MANAGER_TEST_COMPONENT, DATA_MANAGER_TEST_METRIC)
        if newData != startData:
            dataIsTheSame = False
            endTime = time.time()
        time.sleep(0.1) # Small sleep to not kill the cpu
    
    # Raise exception when the data hasn't changed
    if dataIsTheSame:
        raise Exception("Data Manager Test failed after the timeout")
    
    log.info("Data Manager Test has passed")
    log.info("Updating took % seconds", endTime - startTime)

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
        testDataManager()


        startTimeIterations = time.time()
        testRateSpeed(MAX_TEST_ITERATIONS, ITERATION_TEST_SPEED)
        endTime = time.time()


        estimatedTime = MAX_TEST_ITERATIONS * (ITERATION_TEST_SPEED / 1000)
        diffTime = estimatedTime - (endTime - startTimeIterations)
        log.info("Completed Test with {0} iterations over {1} seconds".format(MAX_TEST_ITERATIONS, endTime - startTimeIterations ))
        log.info("Estimated Time was {0} seconds, which is only {1} seconds off the actual results".format(estimatedTime, diffTime))
        log.info("Whole test finished in {} seconds".format(endTime - startTimeTest))


if __name__ == '__main__':
    setup_logger(LOG_TO_CONSOLE, LOG_TO_FILE, LOGGINGLEVEL, LOG_SERVER, LOG_GATHERING)
    DatabaseOpenHelper().on_create()


    gatherThread = start_gather_thread()
    testThread = start_test_thread()
    while testThread.isAlive() and gatherThread.isAlive():
        time.sleep(1) # Main Thread cannot die apparently

    log.info("Testing has concluded, goodbye!")