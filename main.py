from gathering.gather_main import GatherThread
import server.__management as server
import database.dbtest as tst


def start_gather_thread():
    print("Starting up the gathering thread.")

    gather_thread = GatherThread()
    gather_thread.daemon = True
    gather_thread.start()


def start_server():
    """
        Sets up and schedules the start of the web server
    """
    server.start()


if __name__ == '__main__':
    start_gather_thread()
    start_server()

    tst.run_me()
