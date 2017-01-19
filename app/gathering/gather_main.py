"""
 Main file for the gathering thread

 24.08.2016
"""

import logging
import threading
import time


from misc.constants import GATHERING_QUEUELISTENER_DELAY, GATHERING_PERFORMANCE_LOG_DELAY, \
                           GATHERING_LOOP_SLEEP
import misc.queue_manager as queue_manager
from gathering.gatherer_manager import GathererManager
from application_settings.logging_settings import LoggingSettings

log = logging.getLogger("opserv.gathering")
log.setLevel(logging.DEBUG)


class GatherThread(threading.Thread):
    ''' Thread for the gathering backend. Handles the collection of the data '''

    def __init__(self):
        """
            Main Init function for the gathering thread
        """
        log.debug("Initializing GatherThread...")
        threading.Thread.__init__(self)
        GathererManager.init_manager()

        self.running = True


    def run(self):
        """
            Starts the whole gathering process by manually
            starting the queue_listener and then waiting for updates
        """
        log.debug("GatherThread running...")
        # Gathering Loop will be indefinite
        last_queue_time = time.time()
        last_performance_time = time.time()
        while 1:
            if not self.running:
                break
            GathererManager.check_for_expired_events()
            current_time = time.time()
            if current_time - last_queue_time >= GATHERING_QUEUELISTENER_DELAY:
                self.queue_listener()
                last_queue_time = time.time()
            if LoggingSettings.get_setting(LoggingSettings.KEY_LOG_USAGE):
                if current_time - last_performance_time >= GATHERING_PERFORMANCE_LOG_DELAY:
                    log.info("Currently active gatherers: %d", GathererManager.get_gatherer_count())
                    log.info("Gatherer Gathertimes: %s", str(GathererManager.get_measuring_times()))
                    last_performance_time = time.time()
            # To keep CPU usage low, the loop has to sleep atleast a bit
            time.sleep(GATHERING_LOOP_SLEEP)

        # This point shouldn't be reached
        log.debug("Gathering Thread shutting down")
        return

    def queue_listener(self):
        """
            Task that is called by the event scheduler and checks for new messages within the queues
        """

        # Check the set_gathering_rate_queue for any new messages
        while not queue_manager.set_gathering_rate_queue.empty():
            new_rate = queue_manager.set_gathering_rate_queue.get(False)
            GathererManager.handle_new_rate(new_rate)

        # Check the request_data_queue for any new messages
        while not queue_manager.request_data_queue.empty():
            new_request = queue_manager.request_data_queue.get(False)
            GathererManager.handle_data_request(new_request)
