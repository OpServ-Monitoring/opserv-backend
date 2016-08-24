from gathering.gather_main import GatherThread
import server.main


def start_gather_thread():
    print("Starting up the gathering thread.")

    gather_thread = GatherThread()
    gather_thread.daemon = True
    gather_thread.start()


def start_server():
    server.main.start()


if __name__ == '__main__':
    start_gather_thread()
    start_server()
