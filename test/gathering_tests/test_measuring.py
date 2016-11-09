import logging
import threading
import time
import sys
from test_general import start_gather_thread, mock_db_open

import misc.queue_manager as queue_manager
import misc.data_manager as data_manager
from misc.constants import implemented_hardware, HARDWARE_DEFAULTS, SYSTEM_METRICS_TO_COMPS
import pytest

DATA_TEST_TIMEOUT = 5

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
        queue_manager.set_gathering_rate(test_comp, test_metric, 500)
        time.sleep(1)
        queue_manager.set_gathering_rate(test_comp, test_metric, 0)

        # Add some extra sleep to ensure no function is still inserting data into the queue
        time.sleep(0.5)

        # Empty the whole queue
        while queue_manager.read_measurement_from_queue(test_comp, test_metric) is not None:
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
            if HARDWARE_DEFAULTS[hw][0] and HARDWARE_DEFAULTS[hw][1] is not None:
                queue_manager.request_data_queue.put({"component": hw, "metric": met,
                                                      "args": HARDWARE_DEFAULTS[hw][1]})
                queue_manager.get_queue(hw, met,
                                        HARDWARE_DEFAULTS[hw][1]).get(timeout=DATA_TEST_TIMEOUT)
            elif not HARDWARE_DEFAULTS[hw][0]:
                queue_manager.request_data_queue.put({"component": hw, "metric": met})
                queue_manager.get_queue(hw, met).get(timeout=DATA_TEST_TIMEOUT)


# Check that system gathering is always a list
def test_system_is_list():
    '''
        Test that the system gathering data is always list type
    '''
    mock_db_open()
    with start_gather_thread() as t:
        for metric in implemented_hardware["system"]:
            queue_manager.request_data("system", metric)
            return_type = type(queue_manager.read_measurement_from_queue("system", metric,
                                                                         blocking=True)["value"])
            assert return_type == type(list())
    return


@pytest.mark.skipif(sys.platform != 'win32',
                    reason="does not run on windows")
def test_ohm():
    from gathering.measuring.ohm_source import OHMSource
    ohm = OHMSource()
    if ohm.can_measure("cpu", "temperature"):
        newTemp = ohm.get_measurement("cpu", "temperature", "0")
    ohm.deinit()


def test_advanced_all_components():
    '''
        Similar test to test all components, but here all the arguments are gathered aswell
        and are used to really test all the available hardware
    '''
    # Get available args for each componennt
    # RequestData for each comp/arg/metric only do one process
    # Wait for a queue entry for each combo
    SYSTEM_DATA_TIMEOUT = 6
    mock_db_open()
    with start_gather_thread() as t:
        available_args = {}
        for component in implemented_hardware["system"]:
            queue_manager.request_data("system", component)
            new_args = queue_manager.read_measurement_from_queue("system", component,
                                                                 None, True, SYSTEM_DATA_TIMEOUT)
            available_args[SYSTEM_METRICS_TO_COMPS[component]] = new_args["value"]

        # Specifically add memory
        available_args["memory"] = [None]

        # For each component in the system
        for comp in available_args:
            # For each possible argument in the
            for i, arg in enumerate(available_args[comp]):
                # Only check one process and only the third process in the list
                if not (comp == "process" and i != 3):
                    for metric in implemented_hardware[comp]:
                        queue_manager.request_data(comp, metric, arg)
                        result = queue_manager.read_measurement_from_queue(comp, metric, arg, True,
                                                                           SYSTEM_DATA_TIMEOUT)
                    log.info("result: %s", result)


def test_psutil_network():
    '''
        Tests the Psutil MeasuringSource directly
        Currently only then network measures
    '''
    from gathering.measuring.psutil_source import PsUtilWrap
    ps = PsUtilWrap()
    all_netif = ps.get_measurement("system", "networks", None)
    for netif in all_netif:
        log.info(ps.get_measurement("network", "receivepersec", netif))
        log.info(ps.get_measurement("network", "transmitpersec", netif))
        log.info(ps.get_measurement("network", "info", netif))
        time.sleep(0.5)

# Get System Data, and test everything ADVANCED

# Test measuring wrong metric, component or argument
