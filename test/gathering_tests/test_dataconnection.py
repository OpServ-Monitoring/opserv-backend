import logging
import time
from test_general import start_gather_thread, mock_db_open

import misc.queue_manager as queue_manager
import misc.data_manager as data_manager
from database.database_open_helper import DatabaseOpenHelper   

DATA_MANAGER_TIMEOUT = 5
DATA_MANAGER_TEST_COMPONENT = "cpu"
DATA_MANAGER_TEST_METRIC = "usage"


log = logging.getLogger("opserv.test")
log.setLevel(logging.DEBUG)


def start_datamanager():
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


# Unit Test Set Gathering Queue
def test_queue_setgathering():
    test_component = "cpu"
    test_metric = "usage"
    test_delayms = 1000
    test_args = "5"
    
    # First test with args
    queue_manager.setGatheringRate(test_component, test_metric, test_delayms, test_args)
    result = queue_manager.setGatheringRateQueue.get(False)
    if not result["component"] == test_component:
        raise ValueError("Wrong Component in queue{}".format(str(result)))
    if not result["metric"] == test_metric:
        raise ValueError("Wrong metric in queue{}".format(str(result)))
    if not result["delayms"] == test_delayms:
        raise ValueError("Wrong delayms in queue{}".format(str(result)))
    if not result["args"] == test_args:
        raise ValueError("Wrong args in queue{}".format(str(result)))

    # Second test without args
    queue_manager.setGatheringRate(test_component, test_metric, test_delayms)
    result = queue_manager.setGatheringRateQueue.get(False)
    if not result["component"] == test_component:
        raise ValueError("Wrong Component in queue{}".format(str(result)))
    if not result["metric"] == test_metric:
        raise ValueError("Wrong metric in queue{}".format(str(result)))
    if not result["delayms"] == test_delayms:
        raise ValueError("Wrong delayms in queue{}".format(str(result)))

    return


# Unit Test RequestDataQueue
def test_queue_datarequest():
    test_component = "cpu"
    test_metric = "usage"
    test_args = "5"
    
    # First test with args
    queue_manager.requestData(test_component, test_metric, test_args)
    result = queue_manager.requestDataQueue.get(False)
    if not result["component"] == test_component:
        raise ValueError("Wrong Component in queue{}".format(str(result)))
    if not result["metric"] == test_metric:
        raise ValueError("Wrong metric in queue{}".format(str(result)))
    if not result["args"] == test_args:
        raise ValueError("Wrong args in queue{}".format(str(result)))

    # Second test without args
    queue_manager.requestData(test_component, test_metric)
    result = queue_manager.requestDataQueue.get(False)
    if not result["component"] == test_component:
        raise ValueError("Wrong Component in queue{}".format(str(result)))
    if not result["metric"] == test_metric:
        raise ValueError("Wrong metric in queue{}".format(str(result)))

    return


# Unit Test realtime_queues
def test_queue_realtime():
    test_component = "cpu"
    test_metric = "usage"
    test_measurement = {
        "value" : 50,
        "timestamp" : time.time()
    }
    test_args = "5"

    # First test with args    
    queue_manager.putMeasurementIntoQueue(test_component, test_metric, test_measurement, test_args)
    result = queue_manager.readMeasurementFromQueue(test_component, test_metric, test_args)
    if not result == test_measurement:
        raise ValueError("Measurement read from queue was wrong")

    # Second test without args
    queue_manager.putMeasurementIntoQueue(test_component, test_metric, test_measurement)
    result = queue_manager.readMeasurementFromQueue(test_component, test_metric)
    if not result == test_measurement:
        raise ValueError("Measurement read from queue was wrong")


# Unit Test Datamanager realtime data
def test_data_manager():
    test_component = "cpu"
    test_metric = "usage"
    test_measurement = {
        "value" : 50,
        "timestamp" : time.time()
    }
    test_args = "5"


    # First test with args
    result = data_manager.getMeasurement(test_component, test_metric, test_args)
    if result != None:
        raise ValueError("Starting value should always be None")
    data_manager.setMeasurement(test_component, test_metric, test_measurement, test_args)

    result = data_manager.getMeasurement(test_component, test_metric, test_args)
    if result != test_measurement:
        raise ValueError("Measurement read from queue was wrong")

    # Then Test without args
    result = data_manager.getMeasurement(test_component, test_metric)
    if result != None:
        raise ValueError("Starting value should always be None")
    data_manager.setMeasurement(test_component, test_metric, test_measurement)
    result = data_manager.getMeasurement(test_component, test_metric)
    if result != test_measurement:
        raise ValueError("Measurement read from queue was wrong")

# System Test Data Manager
def test_datamanager_gathering():
    mock_db_open() 
    with start_gather_thread() as t:
        start_datamanager()
    return
    
# System Test Queue Manager
def test_queuemanager_gathering():
    pass
