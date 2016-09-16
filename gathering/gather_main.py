#
# Main file for the gathering thread
#
# 24.08.2016
#
#

import threading
import time
import sched
import queue_manager
import logging
from common.helper import importIfExists

# Optional depency importing
psutil = importIfExists("psutil")
pynvml = importIfExists("pynvml")
pyspectator = importIfExists("pyspectator")

log = logging.getLogger("opserv.gathering")
log.setLevel(logging.DEBUG)

class GatherThread(threading.Thread):
    def __init__(self):
        """
            Main Init function for the gathering thread
        """
        log.debug("Initializing GatherThread...")
        threading.Thread.__init__(self)
        self.s = sched.scheduler(time.time, time.sleep)
        self.gatherers = {}
        return

    def run(self):
        """
            Starts the whole gathering process by manually starting the queueListener and then waiting for updates
        """
        global MEASURE_DELAY
        log.debug("GatherThread running...")
        self.s.enter(1, 1, self.queueListener)
        # Gathering Loop will be indefinite
        while 1:
            self.s.run()
            time.sleep(0.05) # To keep CPU usage low, the loop has to sleep atleast a bit
        
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
                if self.alreadyGathering(newRate):
                    self.updateGatherer(newRate)
                else:
                    self.createGatherer(newRate)

        # Check the requestDataQueue for any new messages
        while not queue_manager.requestDataQueue.empty():
            newRequest = queue_manager.requestDataQueue.get(False)
            if requestValid(newRequest):
                newMeasurement = self.getMeasurement(newRequest["hardware"], newRequest["valueType"], newRequest["args"])

                queue = queue_manager.getQueue(newRequest["hardware"], newRequest["valueType"], newRequest["args"])

                queue.put(newMeasurement)

                log.debug("Gathered {0} from {1},{2},{3}".format(newMeasurement, newRequest["hardware"], newRequest["valueType"], newRequest["args"]))
            self.s.enter(1, 1, self.queueListener)

        # Reenter itself into the event queue to listen to new commands
        self.s.enter(1, 1, self.queueListener)


    def getMeasurement(self, hardware, valueType, args):
        """
            Given the hardware and valueType this function uses the libraries to make a measurement
            Returns: The value of the measurement
        """
        # Lowercase to avoid any case errors
        hardware = hardware.lower()
        valueType = valueType.lower()
        if hardware == "cpu":
            if valueType == "load":
                return psutil.cpu_percent()
            elif valueType == "cores":
                return psutil.cpu_count()
        elif hardware == "memory":
            if valueType == "total":
                return psutil.virtual_memory().total
            elif valueType == "free":
                return psutil.virtual_memory().available
            elif valueType == "used":
                return psutil.virtual_memory().used
        elif hardware == "disk":
            if valueType == "partitions":
                return str(psutil.disk_partitions())
        elif hardware == "process":
            if valueType == "getall":
                return str(psutil.pids())
        elif hardware == "system":
            if valueType == "cpus":
                return 1
            if valueType == "cores":
                return psutil.cpu_count()
            if valueType == "gpus":
                return 1
            if valueType == "disks":
                return str(psutil.disk_partitions())
        
        log.debug("Tried to get unimplemented hardware/measurementType")
        return "0"


    def gatherTask(self, gatherData):
        """
            Tasks for the gathering of measurements at a specific rateUpdateValid
            Returns nothing, but sends data to the realtime queue
        """
        newData = self.getMeasurement(gatherData["hardware"], gatherData["valueType"], gatherData["args"])

        queue = queue_manager.getQueue(gatherData["hardware"], gatherData["valueType"], gatherData["args"])
        queue.put(newData)
        log.debug("Gathered {0} from {1},{2}".format(newData, gatherData["hardware"], gatherData["valueType"]))
        self.createGatherer(gatherData)

    def updateGatherer(self, newRate):
        """
            Updates the given gathering task to the new rate (or deletes it)
        """
        # Remove old scheduled event
        self.s.cancel(self.gatherers[(newRate["hardware"], newRate["valueType"])])
        if newRate["delayms"] > 0: 
            self.createGatherer(newRate)


    def createGatherer(self, newRate):
        """
            Creates a new gathering task by entering it as a event for the scheduler
        """
        if newRate["delayms"] > 0:
            self.gatherers[(newRate["hardware"], newRate["valueType"])] = self.s.enter(newRate["delayms"] / 1000, 1, self.gatherTask, kwargs={"gatherData" : newRate})
        else:
            log.debug("ERROR: Tried to create gatherer with a delay of 0")

    def alreadyGathering(self, rateToCheck):
        """
            Checks for a given hardware and valueType combination whether it is already been monitored
            Return True if it is already in the gatherers list
        """
        if (rateToCheck["hardware"], rateToCheck["valueType"]) in self.gatherers:
            return True
        return False



def requestValid(request):
    """
        Checks the given request for the correct data structure
        Returns True if it has the right structure
    """
    if request != None:
        if "hardware" in request and "valueType" in request:
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
        if "hardware" in rateUpdate and "valueType" in rateUpdate and "delayms" in rateUpdate:
            if "args" in rateUpdate:
                return True
            else:
                rateUpdate["args"] = None
                return True
            return True
    log.debug("Rate Update was invalid")
    return False