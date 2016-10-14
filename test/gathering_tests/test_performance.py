import logging
import time

import misc.data_manager as data_manager
import misc.queue_manager as queue_manager
from test_general import mock_db_open, start_gather_thread

MAX_TEST_ITERATIONS = 10
ITERATION_TEST_SPEED = 500

SPEEDTEST_ITERATION_TIMEPRECISION = 100 # Iteration should be hit with +- 100ms precision^


log = logging.getLogger("opserv.test")
log.setLevel(logging.DEBUG)


def test_gathering_speed():
    '''
        Tests gathering speed of the gatherthread and will
        raise exceptions when a specified timeout threshold
        is reached
    '''
    # Setup test constants
    test_delayms = 500
    test_iterations = 11
    lowest_delay = test_delayms - SPEEDTEST_ITERATION_TIMEPRECISION
    highest_delay = test_delayms + SPEEDTEST_ITERATION_TIMEPRECISION
    test_queue_timeout = test_delayms * 2
    mock_db_open()
    with start_gather_thread() as t:
        # Add Gathering Rate
        speedtest_insert_gatherings(test_delayms)

        # Setup test variables
        current_iterations = 0
        start_time = time.time()
        iteration_time = time.time()

        # Handle the immediate set gathering response
        queue_manager.readMeasurementFromQueue("cpu", "usage", None, True,
                                               (test_delayms + test_queue_timeout)/1000) 
        current_iterations += 1
        duration = (time.time() - iteration_time) * 1000
        duration_list = [duration]
        log.debug("First Queue Time (should be pretty immediate): %s", duration)
        assert 0 <= duration < SPEEDTEST_ITERATION_TIMEPRECISION
        iteration_time = time.time()

        # Repeat getting reading measurements until the max iterations are reached
        while current_iterations < test_iterations:
            queue_manager.readMeasurementFromQueue("cpu", "usage", None, True,
                                                   (test_delayms + test_queue_timeout)/1000)
            # Calculate duration of this iterations
            duration = (time.time() - iteration_time) * 1000
            iteration_time = time.time() # Get the new time as fast as possible
            duration_list.append(duration)
            log.debug("Min Delay: %dms, Max Delay: %dms, Measured Delay: %fms, Current Iterations: %d",
                      lowest_delay, highest_delay, duration, current_iterations)

            # Special case for the second iterations,
            # since the timings aren't caught by the scheduler
            # Assert that the duration is within the threshold
            if current_iterations == 1:
                assert lowest_delay < duration < highest_delay + SPEEDTEST_ITERATION_TIMEPRECISION
            else:
                assert lowest_delay < duration < highest_delay
            current_iterations += 1


        test_duration = time.time() - start_time
        # Ignore the first iteration in the calculation since it is immediate
        estimated_time = ((test_iterations - 1) * test_delayms) / 1000
        log.debug("Duration List: %s", str(duration_list))
        log.debug("Estimated Time: %fs", estimated_time)
        log.debug("Total Time: %fs", test_duration)

    return



def speedtest_insert_gatherings(delayms):
    queue_manager.setGatheringRate("cpu", "usage", delayms)

# Test Gathering Speed Basic

# Test Gathering Speed with n simultanous different gathering requests
