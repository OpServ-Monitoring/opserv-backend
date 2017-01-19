import logging
import time

from test_general import start_gather_thread, mock_db_open

import misc.data_manager as data_manager
import misc.queue_manager as queue_manager

DATA_MANAGER_TIMEOUT = 5
DATA_MANAGER_TEST_COMPONENT = "cpu"
DATA_MANAGER_TEST_METRIC = "usage"

log = logging.getLogger("opserv.test")
log.setLevel(logging.DEBUG)


# Unit Test Set Gathering Queue
def test_queue_setgathering():
    test_component = "cpu"
    test_metric = "usage"
    test_delayms = 1000
    test_args = "5"

    # First test with args
    queue_manager.set_gathering_rate(test_component, test_metric, test_delayms, test_args)
    result = queue_manager.set_gathering_rate_queue.get(False)
    if not result["component"] == test_component:
        raise ValueError("Wrong Component in queue{}".format(str(result)))
    if not result["metric"] == test_metric:
        raise ValueError("Wrong metric in queue{}".format(str(result)))
    if not result["delayms"] == test_delayms:
        raise ValueError("Wrong delayms in queue{}".format(str(result)))
    if not result["args"] == test_args:
        raise ValueError("Wrong args in queue{}".format(str(result)))

    # Second test without args
    queue_manager.set_gathering_rate(test_component, test_metric, test_delayms)
    result = queue_manager.set_gathering_rate_queue.get(False)
    if not result["component"] == test_component:
        raise ValueError("Wrong Component in queue{}".format(str(result)))
    if not result["metric"] == test_metric:
        raise ValueError("Wrong metric in queue{}".format(str(result)))
    if not result["delayms"] == test_delayms:
        raise ValueError("Wrong delayms in queue{}".format(str(result)))

    return


# Unit Test request_data_queue
def test_queue_datarequest():
    test_component = "cpu"
    test_metric = "usage"
    test_args = "5"

    # First test with args
    queue_manager.request_data(test_component, test_metric, test_args)
    result = queue_manager.request_data_queue.get(False)
    if not result["component"] == test_component:
        raise ValueError("Wrong Component in queue{}".format(str(result)))
    if not result["metric"] == test_metric:
        raise ValueError("Wrong metric in queue{}".format(str(result)))
    if not result["args"] == test_args:
        raise ValueError("Wrong args in queue{}".format(str(result)))

    # Second test without args
    queue_manager.request_data(test_component, test_metric)
    result = queue_manager.request_data_queue.get(False)
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
        "value": 50,
        "timestamp": time.time()
    }
    test_args = "5"

    # First test with args    
    queue_manager.put_measurement_into_queue(test_component, test_metric, test_measurement, test_args)
    result = queue_manager.read_measurement_from_queue(test_component, test_metric, test_args)
    if not result == test_measurement:
        raise ValueError("Measurement read from queue was wrong")

    # Second test without args
    queue_manager.put_measurement_into_queue(test_component, test_metric, test_measurement)
    result = queue_manager.read_measurement_from_queue(test_component, test_metric)
    if not result == test_measurement:
        raise ValueError("Measurement read from queue was wrong")


# Unit Test Datamanager realtime data
def test_data_manager():
    test_component = "cpu"
    test_metric = "usage"
    test_measurement = {
        "value": 50,
        "timestamp": time.time()
    }
    test_args = "5"

    # First test with args
    result = data_manager.get_measurement(test_component, test_metric, test_args)
    if result is not None:
        raise ValueError("Starting value should always be None")
    data_manager.set_measurement(test_component, test_metric, test_measurement, test_args)

    result = data_manager.get_measurement(test_component, test_metric, test_args)
    if result != test_measurement:
        raise ValueError("Measurement read from queue was wrong")

    # Then Test without args
    result = data_manager.get_measurement(test_component, test_metric)
    if result is not None:
        raise ValueError("Starting value should always be None")
    data_manager.set_measurement(test_component, test_metric, test_measurement)
    result = data_manager.get_measurement(test_component, test_metric)
    if result != test_measurement:
        raise ValueError("Measurement read from queue was wrong")


def start_datamanager():
    '''
        Inserts a gathering rate and test wether the data manager measurement changes
        accordingly
    '''
    log.info("Starting Data Manager Test")

    # Disable any gathering rates for the tested component to avoid any wrong results
    queue_manager.set_gathering_rate(DATA_MANAGER_TEST_COMPONENT, DATA_MANAGER_TEST_METRIC, 0)

    # Save the current value in the realtime data dictionary
    startData = data_manager.get_measurement(DATA_MANAGER_TEST_COMPONENT, DATA_MANAGER_TEST_METRIC)

    # Ask for a data update
    queue_manager.request_data(DATA_MANAGER_TEST_COMPONENT, DATA_MANAGER_TEST_METRIC)
    startTime = time.time()
    dataIsTheSame = True

    # Wait till the new one arrives or timeout expires
    while time.time() - startTime < DATA_MANAGER_TIMEOUT and dataIsTheSame:
        newData = data_manager.get_measurement(DATA_MANAGER_TEST_COMPONENT, DATA_MANAGER_TEST_METRIC)
        if newData != startData:
            dataIsTheSame = False
            endTime = time.time()
        time.sleep(0.1)  # Small sleep to avoid killing the cpu

    # Raise exception when the data hasn't changed
    if dataIsTheSame:
        raise Exception("Data Manager Test failed after the timeout")


# System Test Data Manager
def test_datamanager_gathering():
    mock_db_open()
    with start_gather_thread() as t:
        start_datamanager()
    return


# System Test Queue Manager
def test_queuemanager_gathering():
    pass
