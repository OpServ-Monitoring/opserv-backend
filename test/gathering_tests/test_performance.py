import logging
import time
from test_general import start_gather_thread, mock_db_open

import misc.queue_manager as queue_manager
import misc.data_manager as data_manager

MAX_TEST_ITERATIONS = 10
ITERATION_TEST_SPEED = 500

SPEEDTEST_QUEUE_TIMEOUTPRECISION = 250
SPEEDTEST_ITERATION_TIMEPRECISION = 100 # Iteration should be hit with +- 100ms precision^


log = logging.getLogger("opserv.test")
log.setLevel(logging.DEBUG)


def test_gathering_speed():
    test_delayms = 1000
    test_iterations = 10
    lowest_delay = test_delayms - SPEEDTEST_ITERATION_TIMEPRECISION
    highest_delay = test_delayms + SPEEDTEST_ITERATION_TIMEPRECISION

    mock_db_open()
    with start_gather_thread() as t:
        # Add Gathering Rates
        speedtest_insert_gatherings(test_delayms)
        # Look for new data until timeout or iterations are reached
        current_iterations = 0
        start_time = time.time()
        iteration_time = time.time()

        # Handle the immediate set gathering response
        queue_manager.readMeasurementFromQueue("cpu","usage",None,True, test_delayms + SPEEDTEST_QUEUE_TIMEOUTPRECISION)
        current_iterations += 1
        duration = (time.time() - iteration_time) * 1000
        iteration_time = time.time()
        assert(0 <= duration < SPEEDTEST_ITERATION_TIMEPRECISION)
        while current_iterations < test_iterations:
            queue_manager.readMeasurementFromQueue("cpu","usage",None,True, test_delayms + SPEEDTEST_QUEUE_TIMEOUTPRECISION)
            newTime = time.time()
            duration = (newTime - iteration_time) * 1000
            print(lowest_delay, duration, highest_delay)
            assert(lowest_delay < duration < highest_delay)
            iteration_time = time.time()
            current_iterations += 1
        
        # See if test time is adequate
    return



def speedtest_insert_gatherings(delayms):
    queue_manager.setGatheringRate("cpu", "usage", delayms)

# Test Gathering Speed Basic

# Test Gathering Speed with n simultanous different gathering requests

