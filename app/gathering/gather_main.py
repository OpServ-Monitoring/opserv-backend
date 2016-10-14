#
# Main file for the gathering thread
#
# 24.08.2016
#
#

import logging
import sched
import threading
import time

import misc.queue_manager as queue_manager
import misc.data_manager as data_manager
from misc.constants import GATHERING_QUEUELISTENER_DELAY
from gathering.measuring.measure_main import measure_core, measure_cpu, measure_disk, \
    measure_gpu, measure_memory, measure_network, measure_partition, measure_process, \
    get_system_data
from database.unified_database_interface import UnifiedDatabaseInterface

log = logging.getLogger("opserv.gathering")
log.setLevel(logging.DEBUG)

transaction = UnifiedDatabaseInterface.get_measurement_insertion_transaction()


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
        return

    def run(self):
        """
            Starts the whole gathering process by manually starting the queueListener and then waiting for updates
        """
        log.debug("GatherThread running...")
        self.s.enter(GATHERING_QUEUELISTENER_DELAY, 1, self.queueListener)
        # Gathering Loop will be indefinite
        while 1:
            if not self.running:
                break
            self.s.run(blocking=False)
            time.sleep(0.001)  # To keep CPU usage low, the loop has to sleep atleast a bit

        # This point shouldn't be reached
        log.debug("Gathering Thread shutting down")
        return

    def queueListener(self):
        """
            Task that is called by the event scheduler and checks for new messages within the queues
        """

        # Check the setGatheringRateQueue for any new messages
        while not queue_manager.setGatheringRateQueue.empty():
            newRate = queue_manager.setGatheringRateQueue.get(False)
            if rateUpdateValid(newRate):
                # Before even setting up a new gatherer, send an immediate data update
                getMeasurementAndSend(newRate["component"], newRate["metric"],
                                                     newRate["args"])
                
                if self.alreadyGathering(newRate):
                    self.updateGatherer(newRate)
                else:
                    self.createGatherer(newRate)

        # Check the requestDataQueue for any new messages
        while not queue_manager.requestDataQueue.empty():
            newRequest = queue_manager.requestDataQueue.get(False)
            if requestValid(newRequest):

                getMeasurementAndSend(newRequest["component"], newRequest["metric"],
                                                     newRequest["args"])
  
        # Reenter itself into the event queue to listen to new commands
        self.s.enter(GATHERING_QUEUELISTENER_DELAY, 1, self.queueListener)


    def gatherTask(self, gatherData):
        """
            Tasks for the gathering of measurements at a specific rateUpdateValid
            Returns nothing, but sends data to the realtime queue
            Gatherers are created before the actual measurement to ensure a relatively
            precise timing. (This way measurement computation time
            doesn't affect the gathering rate)
        """

        self.createGatherer(gatherData)
        getMeasurementAndSend(gatherData["component"], gatherData["metric"], gatherData["args"])

    def updateGatherer(self, newRate):
        """
            Updates the given gathering task to the new rate (or deletes it)
        """
        # Remove old scheduled event
        self.s.cancel(self.gatherers[(newRate["component"], newRate["metric"])])
        self.gatherers.pop((newRate["component"], newRate["metric"]))
        if newRate["delayms"] > 0:
            self.createGatherer(newRate)

    def createGatherer(self, newRate):
        """
            Creates a new gathering task by entering it as a event for the scheduler
        """
        if newRate["delayms"] > 0:
            self.gatherers[(newRate["component"], newRate["metric"])] = self.s.enter(newRate["delayms"] / 1000, 1,
                                                                                       self.gatherTask,
                                                                                       kwargs={"gatherData": newRate})
        else:
            log.debug("ERROR: Tried to create gatherer with a delay of 0")

    def alreadyGathering(self, rateToCheck):
        """
            Checks for a given component and metric combination whether it is already been monitored
            Return True if it is already in the gatherers list
        """
        if (rateToCheck["component"], rateToCheck["metric"]) in self.gatherers:
            return True
        return False

def getMeasurementAndSend(component, metric, args):
    """ Gets the specified metric from the component and sends it into the queue and data dictionary """
    # Get the data
    try:
        newData = getMeasurement(component, metric, args)
    except Exception as e:
        log.error(e)
        log.error("CATCHED MEASUREMENT ERROR")
        return
    # Put that data into the queue
    queue_manager.putMeasurementIntoQueue(component, metric, newData, args)

    # Update the data in the realtime dictionary
    data_manager.setMeasurement(component, metric, newData, args)

    # Save data to the Database
    transaction.insert_measurement(metric, newData["timestamp"], str(newData["value"]), component, args)
    transaction.commit_transaction()

    log.debug("Gathered {0} from {1},{2},{3}".format(newData, component, metric, args))


def requestValid(request):
    """
        Checks the given request for the correct data structure
        Returns True if it has the right structure
    """
    if request != None:
        if "component" in request and "metric" in request:
            if "args" in request:
                return True
            else:
                request["args"] = None
                return True
    log.debug("Request was invalid")
    return False


def rateUpdateValid(rateUpdate):
    """
        Checks the given rateUpdate for the correct data structure
        Returns True if it has the right structure
    """
    if rateUpdate != None:
        if "component" in rateUpdate and "metric" in rateUpdate and "delayms" in rateUpdate:
            if "args" in rateUpdate:
                return True
            else:
                rateUpdate["args"] = None
                return True
            return True
    log.debug("Rate Update was invalid")
    return False



def getMeasurement(component, metric, args):
    """
        Given the component and metric this function uses the libraries to make a measurement
        Returns: The value of the measurement
    """
    # Lowercase to avoid any case errors
    component = component.lower()
    metric = metric.lower()

    measured_value = None
    if component == "cpu":
        measured_value = measure_cpu(metric, args)
    elif component == "memory":
        measured_value = measure_memory(metric, args)
    elif component == "disk":
        measured_value = measure_disk(metric, args)
    elif component == "partition":
        measured_value = measure_partition(metric, args)
    elif component == "process":
        measured_value = measure_process(metric, args)
    elif component == "core":
        measured_value = measure_core(metric, args)
    elif component == "gpu":
        measured_value = measure_gpu(metric, args)
    elif component == "network":
        measured_value = measure_network(metric, args)

    # Server Thread wants this to get basic system information
    elif component == "system":
        measured_value = get_system_data(metric)

    if measured_value != None:
        return {
            "timestamp" : time.time() * 1000,
            "value" : measured_value
        }


    log.debug("Tried to get unimplemented component")
    return "0"
