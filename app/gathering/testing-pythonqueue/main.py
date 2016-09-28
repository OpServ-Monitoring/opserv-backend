import queuetest
import secondary

counter = 0


def writeQueue():
    global counter
    counter += 1
    queuetest.newQueue.put("omg i cant believe this works" + str(counter))


def main():
    writeQueue()
    secondary.readQueue()

    writeQueue()
    secondary.readQueue()

    writeQueue()
    secondary.readQueue()


main()
