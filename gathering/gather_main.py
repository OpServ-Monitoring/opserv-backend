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

MEASURE_DELAY = 0.5

class GatherThread(threading.Thread):
    def __init__(self):
        print("Initializing GatherThread...")
        threading.Thread.__init__(self)
        return

    def run(self):
        global MEASURE_DELAY
        print("GatherThread running...")
        # Gathering Loop will be indefinite
        self.updateTime = time.time()
        while 1:
            self.updateTime = time.time()
            newData = psutil.cpu_percent()
            queueManager.realTimeDataQueue.put(newData)
            print("Pusehd to following CPU-Usage:{}".format(newData))
            # Avoid 100% usage

            time.sleep(MEASURE_DELAY - (time.time() - self.updateTime))
        return
    