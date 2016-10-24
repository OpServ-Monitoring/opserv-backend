import logging
import threading
import time
import sys
from test_general import start_gather_thread, mock_db_open

import misc.queue_manager as queue_manager
import misc.data_manager as data_manager
from misc.constants import implemented_hardware, HARDWARE_DEFAULTS
import pytest


DATA_TEST_TIMEOUT = 2.5


log = logging.getLogger("opserv.test")
log.setLevel(logging.DEBUG)

# Test system gathering more specifically, e.g. check results for fitting structure
def test_system_gathering():
    mock_db_open()
    with start_gather_thread() as t:
        pass
    return


def test_all_components():
    '''
        Tests all components, that don't require an argument
    '''
    mock_db_open()
    with start_gather_thread() as t:
        check_all_hardware()
    return

def test_gathering_delete():
    '''
        Sets a gathering rate and then deletes it
    '''
    test_comp = "cpu"
    test_metric = "usage"

    mock_db_open()
    with start_gather_thread() as t:
        queue_manager.setGatheringRate(test_comp, test_metric, 500)
        time.sleep(1)
        queue_manager.setGatheringRate(test_comp, test_metric, 0)

        # Add some extra sleep to ensure no function is still inserting data into the queue
        time.sleep(0.5)

        # Empty the whole queue
        while queue_manager.readMeasurementFromQueue(test_comp, test_metric) != None:
            pass
        time.sleep(2)

        # Queue Should still be empty
        assert queue_manager.real_time_queue_empty(test_comp, test_metric)

    return


def check_all_hardware():
    '''
        Sends a data request to the gathering backend and immediately checks for response
        The response will be timedout after a certain period of time
    '''
    # For each hardware in the hardware list
    for hw in implemented_hardware:
        # For Each metric of that specific hardware
        for met in implemented_hardware[hw]:
            if HARDWARE_DEFAULTS[hw][0] and HARDWARE_DEFAULTS[hw][1] != None:
                queue_manager.requestDataQueue.put({"component": hw, "metric": met,
                                                    "args" : HARDWARE_DEFAULTS[hw][1]})
                queue_manager.getQueue(hw, met,
                                       HARDWARE_DEFAULTS[hw][1]).get(timeout=DATA_TEST_TIMEOUT)
            elif not HARDWARE_DEFAULTS[hw][0]:
                queue_manager.requestDataQueue.put({"component": hw, "metric": met})
                queue_manager.getQueue(hw, met).get(timeout=DATA_TEST_TIMEOUT)

# Check that system gathering is always a list
def test_system_is_list():
    '''
        Test that the system gathering data is always list type
    '''
    mock_db_open()
    with start_gather_thread() as t:
        for metric in implemented_hardware["system"]:
            queue_manager.requestData("system", metric)
            return_type = type(queue_manager.readMeasurementFromQueue("system", metric,
                                                                      blocking=True)["value"])
            assert return_type == type(list())
    return


@pytest.mark.skipif(sys.platform != 'win32',
                    reason="does not run on windows")
def test_ohm():
    from gathering.measuring.ohm_source import OHMSource
    ohm = OHMSource()
    newTemp = ohm.get_measurement("cpu", "temperature", "0")
    ohm.deinit()

# Get System Data, and test everything ADVANCED

# Test measuring wrong metric, component or argument
