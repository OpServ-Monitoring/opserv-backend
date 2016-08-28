#
# Main file for the gathering thread
#
# 24.08.2016
#
#

import threading
import psutil
import time
import queueManager
import sched


class GatherThread(threading.Thread):
    def __init__(self):
        """
            Main Init function for the gathering thread
        """
        print("Initializing GatherThread...")
        threading.Thread.__init__(self)
        self.s = sched.scheduler(time.time, time.sleep)
        self.gatherers = {}
        return

    def run(self):
        """
            Starts the whole gathering process by manually starting the queueListener and then waiting for updates
        """
        global MEASURE_DELAY
        print("GatherThread running...")
        self.s.enter(1, 1, self.queueListener)
        insertTestDataIntoQueue()
        # Gathering Loop will be indefinite
        while 1:
            self.s.run()
            time.sleep(0.05) # To keep CPU usage low, the loop has to sleep atleast a bit
        
        # This point shouldn't be reached
        print("Gathering Thread shutting down")
        return


    def queueListener(self):
        """
            Task that is called by the event scheduler and checks for new messages within the queues
        """
        
        # Check the setGatheringRateQueue for any new messages
        while not queueManager.setGatheringRateQueue.empty():
            newRate = queueManager.setGatheringRateQueue.get(False)
            if rateUpdateValid(newRate):
                if self.alreadyGathering(newRate):
                    self.updateGatherer(newRate)
                else:
                    self.createGatherer(newRate)

        # Check the requestDataQueue for any new messages
        while not queueManager.requestDataQueue.empty():
            newRequest = queueManager.requestDataQueue.get(False)
            if requestValid(newRequest):
                newMeasurement = self.getMeasurement(newRequest["hardware"], newRequest["measureType"])
                queueManager.realTimeDataQueue.put(newRequest["hardware"], newRequest["measureType"], newMeasurement)
                print("Gathered {0} from {1},{2}".format(newMeasurement, newRequest["hardware"], newRequest["measureType"]))
            self.s.enter(1, 1, self.queueListener)

        # Reenter itself into the event queue to listen to new commands
        self.s.enter(1, 1, self.queueListener)


    def getMeasurement(self, hardware, measureType):
        """
            Given the hardware and measuretype this function uses the libraries to make a measurement
            Returns: The value of the measurement
        """
        # Lowercase to avoid any case errors
        hardware = hardware.lower()
        measureType = measureType.lower()
        if hardware == "cpu":
            if measureType == "load":
                return psutil.cpu_percent()
            elif measureType == "cores":
                return psutil.cpu_count()
        elif hardware == "memory":
            if measureType == "total":
                return psutil.virtual_memory().total
            elif measureType == "free":
                return psutil.virtual_memory().available
            elif measureType == "used":
                return psutil.virtual_memory().used
        elif hardware == "disk":
            if measureType == "partitions":
                return str(psutil.disk_partitions())
        elif hardware == "process":
            if measureType == "getall":
                return str(psutil.pids())
        print("Tried to get unimplemented hardware/measurementType")
        return "0"


    def gatherTask(self, gatherData):
        """
            Tasks for the gathering of measurements at a specific rateUpdateValid
            Returns nothing, but sends data to the realtime queue
        """
        newData = self.getMeasurement(gatherData["hardware"], gatherData["measureType"])
        queueManager.realTimeDataQueue.put(gatherData["hardware"], gatherData["measureType"], newData)
        print("Gathered {0} from {1},{2}".format(newData, gatherData["hardware"], gatherData["measureType"]))
        self.createGatherer(gatherData)

    def updateGatherer(self, newRate):
        """
            Updates the given gathering task to the new rate (or deletes it)
        """
        # Remove old scheduled event
        self.s.cancel(self.gatherers[(newRate["hardware"], newRate["measureType"])])
        if newRate["delayms"] > 0: 
            self.createGatherer(newRate)


    def createGatherer(self, newRate):
        """
            Creates a new gathering task by entering it as a event for the scheduler
        """
        if newRate["delayms"] > 0:
            self.gatherers[(newRate["hardware"], newRate["measureType"])] = self.s.enter(newRate["delayms"] / 1000, 1, self.gatherTask, kwargs={"gatherData" : newRate})
        else:
            print("ERROR: Tried to create gatherer with a delay of 0")

    def alreadyGathering(self, rateToCheck):
        """
            Checks for a given hardware and measureType combination whether it is already been monitored
            Return True if it is already in the gatherers list
        """
        if (rateToCheck["hardware"], rateToCheck["measureType"]) in self.gatherers:
            return True
        return False



def requestValid(request):
    """
        Checks the given request for the correct data structure
        Returns True if it has the right structure
    """
    if request != None:
        if "hardware" in request and "measureType" in request:
            return True
    print("Request was invalid")
    return False


def rateUpdateValid(rateUpdate):
    """
        Checks the given rateUpdate for the correct data structure
        Returns True if it has the right structure
    """
    if rateUpdate != None:
        if "hardware" in rateUpdate and "measureType" in rateUpdate and "delayms" in rateUpdate:
            return True
    print("Rate Update was invalid")
    return False

def insertTestDataIntoQueue():
    """
        Inserts testing data into the gatheringrate and request queues
    """
    queueManager.setGatheringRateQueue.put({"hardware" : "cpu", "measureType" : "load", "delayms" : 1000})
    queueManager.setGatheringRateQueue.put({"hardware" : "memory", "measureType" : "used", "delayms" : 1000})
    queueManager.setGatheringRateQueue.put({"hardware" : "cpu", "measureType" : "cores", "delayms" : 5000})
    queueManager.requestDataQueue.put({"hardware" : "disk", "measureType" : "partitions"})
    queueManager.requestDataQueue.put({"hardware" : "process", "measureType" : "getall"})
    queueManager.setGatheringRateQueue.put({"hardware" : "cpu", "measureType" : "cores", "delayms" : 0})