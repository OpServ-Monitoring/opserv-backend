"""
 Main file for the gathering thread

 24.08.2016

"""

import logging
import sched
import threading
import time

import misc.data_manager as data_manager
import misc.queue_manager as queue_manager
from database.unified_database_interface import UnifiedDatabaseInterface
from gathering.measuring.cpuinfo_source import PyCpuInfoSource
from gathering.measuring.null_source import NullSource
from gathering.measuring.ohm_source import OHMSource
from gathering.measuring.raspi_temp_source import RaspiTempSource
from gathering.measuring.psutil_source import PsUtilWrap
from gathering.measuring.pyspectator_source import PySpectatorSource
from misc.constants import GATHERING_QUEUELISTENER_DELAY

log = logging.getLogger("opserv.gathering")
log.setLevel(logging.DEBUG)

transaction = UnifiedDatabaseInterface.get_measurement_insertion_transaction()

measuring_sources = []


class GatherThread(threading.Thread):
    ''' Thread for the gathering backend. Handles the collection of the data '''

    def __init__(self):
        """
            Main Init function for the gathering thread
        """
        log.debug("Initializing GatherThread...")
        threading.Thread.__init__(self)
        self.s = sched.scheduler(time.time, time.sleep)
        self.running = True
        self.gatherers = {}

        # Get all the available Measuring Sources
        measuring_sources.append(PsUtilWrap())
        measuring_sources.append(PyCpuInfoSource())
        measuring_sources.append(PySpectatorSource())
        measuring_sources.append(OHMSource())
        measuring_sources.append(RaspiTempSource())
        measuring_sources.append(NullSource())
        if not measuring_sources[0].init():
            log.error("Psutil Measuring Source could not be loaded!")
        return

    def run(self):
        """
            Starts the whole gathering process by manually
            starting the queue_listener and then waiting for updates
        """
        log.debug("GatherThread running...")
        self.s.enter(GATHERING_QUEUELISTENER_DELAY, 1, self.queue_listener)
        # Gathering Loop will be indefinite
        while 1:
            if not self.running:
                break
            self.s.run(blocking=False)
            # To keep CPU usage low, the loop has to sleep atleast a bit
            time.sleep(0.001)

        # This point shouldn't be reached
        log.debug("Gathering Thread shutting down")
        return

    def queue_listener(self):
        """
            Task that is called by the event scheduler and checks for new messages within the queues
        """

        # Check the setGatheringRateQueue for any new messages
        while not queue_manager.setGatheringRateQueue.empty():
            new_rate = queue_manager.setGatheringRateQueue.get(False)
            if rate_update_valid(new_rate):
                # Before even setting up a new gatherer, send an immediate data
                # update
                get_measurement_and_send(new_rate["component"], new_rate["metric"],
                                         new_rate["args"])

                if self.already_gathering(new_rate):
                    self.update_gatherer(new_rate)
                else:
                    self.create_gatherer(new_rate)

        # Check the requestDataQueue for any new messages
        while not queue_manager.requestDataQueue.empty():
            newRequest = queue_manager.requestDataQueue.get(False)
            if request_valid(newRequest):
                get_measurement_and_send(newRequest["component"], newRequest["metric"],
                                         newRequest["args"])

        # Reenter itself into the event queue to listen to new commands
        self.s.enter(GATHERING_QUEUELISTENER_DELAY, 1, self.queue_listener)

    def gather_task(self, gatherData):
        """
            Tasks for the gathering of measurements at a specific rateUpdateValid
            Returns nothing, but sends data to the realtime queue
            Gatherers are created before the actual measurement to ensure a relatively
            precise timing. (This way measurement computation time
            doesn't affect the gathering rate)
        """

        self.create_gatherer(gatherData)
        get_measurement_and_send(gatherData["component"], gatherData["metric"], gatherData["args"])

    def update_gatherer(self, new_rate):
        """
            Updates the given gathering task to the new rate (or deletes it)
        """
        # Remove old scheduled event
        self.s.cancel(
            self.gatherers[(new_rate["component"], new_rate["metric"])])
        self.gatherers.pop((new_rate["component"], new_rate["metric"]))
        if new_rate["delayms"] > 0:
            self.create_gatherer(new_rate)

    def create_gatherer(self, new_rate):
        """
            Creates a new gathering task by entering it as a event for the scheduler
        """
        if new_rate["delayms"] > 0:
            self.gatherers[(new_rate["component"],
                            new_rate["metric"])] = self.s.enter(new_rate["delayms"] / 1000, 1,
                                                                self.gather_task,
                                                                kwargs={"gatherData": new_rate})
        else:
            log.debug("ERROR: Tried to create gatherer with a delay of 0")

    def already_gathering(self, rate_to_check):
        """
            Checks for a given component and metric combination whether it is already been monitored
            Return True if it is already in the gatherers list
        """
        if (rate_to_check["component"], rate_to_check["metric"]) in self.gatherers:
            return True
        return False


def get_measurement_and_send(component, metric, args):
    """
        Gets the specified metric from the component and sends it into the queue and data dictionary
    """
    # Get the data
    new_data = get_measurement(component, metric, args)
    # Put that data into the queue
    queue_manager.putMeasurementIntoQueue(component, metric, new_data, args)

    # Update the data in the realtime dictionary
    data_manager.setMeasurement(component, metric, new_data, args)

    # Save data to the Database
    transaction.insert_measurement(metric, new_data["timestamp"],
                                   str(new_data["value"]), component, args)
    transaction.commit_transaction()

    log.debug("Gathered {0} from {1},{2},{3}".format(
        new_data, component, metric, args))


def request_valid(request):
    """
        Checks the given request for the correct data structure
        Returns True if it has the right structure
    """
    if request is not None:
        if "component" in request and "metric" in request:
            if "args" in request:
                return True
            else:
                request["args"] = None
                return True
    log.debug("Request was invalid")
    return False


def rate_update_valid(rateUpdate):
    """
        Checks the given rateUpdate for the correct data structure
        Returns True if it has the right structure
    """
    if rateUpdate is not None:
        if "component" in rateUpdate and "metric" in rateUpdate and "delayms" in rateUpdate:
            if "args" in rateUpdate:
                return True
            else:
                rateUpdate["args"] = None
                return True
            return True
    log.debug("Rate Update was invalid")
    return False


def get_measurement(component, metric, args):
    """
        Given the component and metric this function uses the libraries to make a measurement
        Returns: The value of the measurement
    """
    # Lowercase to avoid any case errors
    component = component.lower()
    metric = metric.lower()

    measured_value = None
    for src in measuring_sources:
        if src.can_measure(component, metric):
            try:
                measured_value = src.get_measurement(component, metric, args)
                break  # Just use the first src that is able to measure
            except Exception as err:
                log.error(err)
                log.error("Measuring failed here %s, %s, %s, %s",
                          component, metric, args, str(src))

    if measured_value is not None:
        return {
            "timestamp": time.time() * 1000,
            "value": measured_value
        }

    log.debug("Tried to get unimplemented component")
    return "0"
