#
# Queue File for using the same queues within the project
#
# 27.08.2016
#
# Example usage:
#
# import queues
# queues.requestDataQueue.put("givememoredata")
# print(queues.requestDataQueue.get())
#

from queue import Queue

requestDataQueue = Queue()
setGatheringRateQueue = Queue()
realTimeDataQueue = Queue()

