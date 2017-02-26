"""
 Main system launch file, creates the gathering thread and starts flask

 27.09.2016

 Usage: Simply launch this file
"""

import ctypes
import os
import sys
import logging

import application_settings.settings_management as app_settings
import misc.data_manager as data_manager
import misc.queue_manager as queue_manager
from server.server_management import ServerManagement
from application_settings.app_settings import AppSettings
from application_settings.configuration_settings import ConfigurationSettings
from database.unified_database_interface import UnifiedDatabaseInterface
from gathering.gather_main import GatherThread
from misc.logging_helper import setup_argparse_logger
from misc.opserv_helper import get_operating_system
from misc.constants import YES_PHRASES

log = logging.getLogger("opserv." + __name__)


# TODO Future version: Evaluate whether all prints should use the log instead or not

# Toggle this if you want to test the new apis
USE_TORNADO = False


def init_database():
    """
        Initiates the database
    """
    database_initializer = UnifiedDatabaseInterface.get_database_initializer()

    database_initializer.create_database()
    database_initializer.set_gathering_rates()
    database_initializer.configure_admin_user()


def start_gather_thread():
    """
        Starts the gathering thread as a daemon
    """
    log.debug("Starting up the gathering thread.")

    gather_thread = GatherThread()
    gather_thread.daemon = True
    gather_thread.start()


def start_server():
    """
        Sets up and schedules the start of the web server
    """
    if USE_TORNADO:
        import threading

        class TestThread(threading.Thread):
            def run(self):

                while 1:
                    import time
                    import random

                    from server.server_management import ServerManagement as test
                    test.broadcast_new_measurement("cpucore", str(random.randint(0, 7)), "usage", time.time() * 1000,
                                                   str(random.randint(0, 100)))
                    time.sleep(1)

        test_thread = TestThread()
        test_thread.daemon = True
        test_thread.start()

        ServerManagement.start_server()
    else:
        import server.__management as legacy_server
        legacy_server.start()


def manage_runtime_settings():
    # TODO Document this function
    app_settings.init()


def has_elevated_privileges():
    '''
        Checks for elevated privileges/admin rights and warns the user if they couldn't
        be detected
    '''
    is_admin = False
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin


def start_app():
    queue_manager.init()
    data_manager.init()

    init_database()

    start_gather_thread()

    start_server()


def skip_welcome():
    """
        Skip welcome message
        To be used lateron
    """
    return False


def skip_info_checks():
    """
        Skip info Checks
        to be used later on
    """
    return False


def skip_config():
    """
        Skip configuration to avoid human interaction
        Important for automation etc.
    """
    if AppSettings.get_setting(AppSettings.KEY_SKIP_CONFIG) or \
            ConfigurationSettings.config_file_is_valid():
        return True
    return False


def show_welcome_screen():
    print(r"""
        Welcome to
         ____        _____                 
        / __ \      / ____|                
        | |  | |_ __| (___   ___ _ ____   __
        | |  | | '_ \\___ \ / _ \ '__\ \ / /
        | |__| | |_) |___) |  __/ |   \ V / 
        \____/ | .__/_____/ \___|_|    \_/  
               | |                          
               |_|                          
        Monitoring made easy
          """)


def show_opserv_info():
    print("Elevated Permissions: " + str(has_elevated_privileges()))
    print("Reported Platform Value: " + sys.platform)
    print("Detected Operating System: " + str(get_operating_system()))
    print("Python Version: " + "{0}.{1}.{2}.{3}".format(sys.version_info.major,
                                                        sys.version_info.minor,
                                                        sys.version_info.micro,
                                                        sys.version_info.releaselevel))
    # TODO Is this needed anymore?
    # print("Internet Access: {0}({1})".format(str(has_internet_access()), get_external_ip()))


def config_setup():
    print("Which port would you like to run the sofware on?")
    port = input()
    print("Do you want to setup SSL automatically? Y/N")
    auto_ssl = input()
    if auto_ssl.lower() in YES_PHRASES:
        start_lets_encrypt_flow()
    else:
        print("Having no SSL setup could compromise your system data")
        print("It is highly recommended setting it up when this app is publicly available")
    print("Enter a passphrase for your monitoring dashboard!")
    passphrase = input()
    print("Writing settings to config file...")

    # TODO Future version: Write settings to config file


def start_lets_encrypt_flow():
    pass


if __name__ == '__main__':
    # Get Arg Settings as well as config file
    manage_runtime_settings()

    # Setup the logger with argparsed settings
    setup_argparse_logger()

    # Show the welcome screen on first startup
    if not skip_welcome():
        show_welcome_screen()

    if not skip_info_checks():
        show_opserv_info()

    if not skip_config():
        config_setup()

    start_app()
