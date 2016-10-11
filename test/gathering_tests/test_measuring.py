import logging
import threading
import time
from test_general import start_gather_thread, mock_db_open
 
import misc.queue_manager as queue_manager
import misc.data_manager as data_manager
from gathering.gather_main import GatherThread
from misc.logging_helper import setup_logger
from misc.constants import implemented_hardware, HARDWARE_DEFAULTS
from database.database_open_helper import DatabaseOpenHelper


DATA_TEST_TIMEOUT = 2.5


log = logging.getLogger("opserv.test")
log.setLevel(logging.DEBUG)


def test_system_gathering():
    mock_db_open()
    with start_gather_thread() as t:
        pass
    return
    
def test_all_components():
    pass
def test_gathering_delete():
    pass




def InsertSystemGathering():
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



def AllHardware():
    # For each hardware in the hardware list
    for hw in implemented_hardware:
        # For Each metric of that specific hardware
        log.info("Testing {}".format(implemented_hardware[hw]))
        for vT in implemented_hardware[hw]:
            if HARDWARE_DEFAULTS[hw][0] and HARDWARE_DEFAULTS[hw][1] != None:
                queue_manager.requestDataQueue.put({"hardware": hw, "metric": vT, "args" : HARDWARE_DEFAULTS[hw][1]})
                queue_manager.getQueue(hw,vT,HARDWARE_DEFAULTS[hw][1]).get(timeout=DATA_TEST_TIMEOUT)
            elif not HARDWARE_DEFAULTS[hw][0]:
                queue_manager.requestDataQueue.put({"hardware": hw, "metric": vT})
                queue_manager.getQueue(hw,vT).get(timeout=DATA_TEST_TIMEOUT)


# Test All hardware that doesn't require an argument

# Get System Data, and test everything ADVANCED

# Test measuring wrong metric, component or argument