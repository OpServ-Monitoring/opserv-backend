'''
    This module contains a wrapper class to create a nice fitting interface to the psutil module
'''

import logging
import time

from gathering.measuring.MeasuringSource import MeasuringSource
from misc.constants import Operating_System
from misc.helper import import_if_exists

log = logging.getLogger("opserv.gathering.psutil")
log.setLevel(logging.DEBUG)

NOTIMPLEMENTED_NUMERICAL = 0
NOTIMPLEMENTED_TEXT = ""


class PsUtilWrap(MeasuringSource):
    '''
        MeasuringSource adaption to the psutil interface
    '''

    _supported_os = [Operating_System.macos,
                     Operating_System.windows, Operating_System.linux]

    _supported_comps = {
        "cpu": {
            "usage"
        },
        "core": {
            "usage"
        },
        "memory": {
            "total",
            "free",
            "used"
        },
        "process": {
            "cpuusage",
            "memusage",
            "name"
        },
        "partition": {
            "total",
            "free",
            "used"
        },
        "network": {
            "info",
            "receivepersec",
            "transmitpersec"
        },
        "system": {
            "cores",
            "partitions",
            "processes",
            "networks"
        }
    }

    def __init__(self):
        self._init_complete = False
        self.psutil = None

        # Network specific fields
        # This contains the latest saved receive and sent bytes data
        # Using this format:
        # {
        #    "wlan1" : {"bytes": 5050, "timestamp": 1231245345.323}
        # }
        # wlan1 is the network interface name as received by the get_network_interfaces function
        # bytes is the numer of bytes got from the system
        # timestamp is the time of the measurement in seconds
        self.net_last_receive_data = {}
        self.net_last_sent_data = {}

        self.init()

    def init(self):
        '''
            Initializes the measuring source (opening hardware connections etc.)
            If initialization is successful, it will return True
            If errors occured, the return value will be False
        '''

        self.psutil = import_if_exists("psutil")

        if not self.psutil:
            return False

        self._init_complete = True
        return True

    def deinit(self):
        '''
            De-Initializes the measuring source, removing connections etc.
            Returns True if deinit was successfull, False if it errord
        '''
        self._init_complete = False
        return True

    def get_measurement(self, component, metric, args):
        '''
            Retrieves a measurement from the measuring source
            given the component, metric and optionally arguments
        '''
        if not self._init_complete:
            log.error("Tried to capture measurement without initialization")
            return None

        if not self.can_measure(component, metric):
            raise NotImplementedError

        result = None
        if component == "cpu":
            if metric == "usage":
                result = self.psutil.cpu_percent(percpu=False)

        elif component == "core":
            if metric == "usage":
                result = self.psutil.cpu_percent(percpu=True)[args]

        elif component == "memory":
            result = self.measure_memory(metric)

        elif component == "process":
            result = self.measure_process(metric, args)

        elif component == "partition":
            result = self.measure_partition(metric, args)
        elif component == "network":
            result = self.measure_network(metric, args)

        elif component == "system":
            result = self.get_system_data(metric)

        return result

    def measure_memory(self, metric):
        '''
            Returns a measurement of the desired system memories metrics
        '''
        if metric == "total":
            return self.psutil.virtual_memory().total
        elif metric == "free":
            return self.psutil.virtual_memory().available
        elif metric == "used":
            return self.psutil.virtual_memory().used

    def measure_process(self, metric, args):
        '''
            Returns a measurement of the desired process and metric
        '''
        requested_process = self.psutil.Process(args)
        if metric == "cpuusage":
            return requested_process.cpu_percent()
        elif metric == "memusage":
            return requested_process.memory_info().rss
        elif metric == "name":
            return requested_process.name()

    def measure_partition(self, metric, args):
        '''
            Returns a measurement of the desired partition and metric
        '''
        try:
            if metric == "total":
                return self.psutil.disk_usage(args).total
            elif metric == "free":
                return self.psutil.disk_usage(args).free
            elif metric == "used":
                return self.psutil.disk_usage(args).used
        except OSError as err:
            log.error(err)
            log.error("Path does not exist: %s", str(args))

    def measure_network(self, metric, args):
        '''
            Returns a measurement of the desired network interface and metric
        '''
        try:
            if metric == "info":
                return str(self.psutil.net_if_stats()[args]) + str(self.psutil.net_if_addrs()[args])
            elif metric == "receivepersec":
                # Check if there is already an entry for this netif
                # If, then check if the bytes went down since last TimeoutError
                # If the bytes went not down, calculate the diff per second
                return self.net_calc_bytesper_sec(True, args)
            elif metric == "transmitpersec":
                return self.net_calc_bytesper_sec(False, args)
        except FileNotFoundError as err:
            log.error(err)
            log.error(
                "The following network interface couldnt be found %s", str(args))

    def net_calc_bytesper_sec(self, received, name):
        '''
           Uses the last received data fields to calculate either the receive or sent
           bytes per second. Returns zero if it couldn't be determined
           Also can raise the FileNotFoundError, if the interface can not be found
        '''
        new_bytes = self.net_get_bytes(received, name)
        new_time = time.time()
        bytes_per_second = 0
        last = {
            "bytes" : 0
        }
        # Get specifc data for received and sent
        if received and name in self.net_last_receive_data:
            last = self.net_last_receive_data[name]
        elif not received and name in self.net_last_sent_data:
            last = self.net_last_sent_data[name]

        # Try to calculate bytes per second
        if last["bytes"] <= new_bytes and last["bytes"] != 0:
            byte_diff = new_bytes - last["bytes"]
            time_diff = new_time - last["timestamp"]
            bytes_per_second = byte_diff / time_diff

        # Save data to thei specific dict entries
        if received:
            self.net_last_receive_data[name] = {
                "bytes": new_bytes,
                "timestamp": new_time
            }
        else:
            self.net_last_sent_data[name] = {
                "bytes": new_bytes,
                "timestamp": new_time
            }
        return bytes_per_second

    def net_get_bytes(self, received, name):
        '''
            Gets either the received or sent (depending on the parameter) bytes from
            the specified network interface
        '''
        networks_list = self.psutil.net_io_counters(pernic=True)
        if name in networks_list:
            if received:
                return getattr(networks_list[name], "bytes_recv")
            else:
                return getattr(networks_list[name], "bytes_sent")
        else:
            raise FileNotFoundError

    def get_system_data(self, metric):
        '''
            Returns a measurement of the specified basic system metric
        '''
        if metric == "cores":
            return self.get_core_list()
        if metric == "partitions":
            return self.get_partition_list()
        if metric == "processes":
            return self.get_process_list()
        if metric == "networks":
            return self.get_network_interfaces()

    def get_network_interfaces(self):
        '''
            Gets the names of all currently available network interfaces
            and returns them in an array
        '''
        if not self.psutil:
            return []
        try:
            detailed_interfaces = self.psutil.net_if_stats()
        except LookupError as error:
            log.error(error)
            log.error("Couldn't get network interfaces")
            detailed_interfaces = {}
        simple_interfaces = []
        for interface in detailed_interfaces:
            simple_interfaces.append(interface)
        return simple_interfaces

    def get_core_list(self):
        '''
            Returns a list of all the available cpu cores
            E.g. 4 Cores: [0,1,2,3]
        '''
        result = []
        try:
            result = list(range(self.psutil.cpu_count()))
        except Exception as error:
            log.error("Couldn't get corelist")
            log.error(error)
        return result
        
    def get_partition_list(self):
        '''
            Returns a list of all the available partitions
            which are basically the mount locations /mnt/SDA1, C:/
        '''
        result = []
        try:
            part_tuples = self.psutil.disk_partitions()
            for part in part_tuples:
                result.append(part.mountpoint)
        except Exception as err:
            log.error("Couldn't get partition list")
            log.error(err)
        return result

    def get_process_list(self):
        '''
            Returns a list of all the currently active processes
            using their PIDs
        '''
        result = []
        try:
            result = self.psutil.pids()
        except Exception as err:
            log.error("Couldn't get processlist")
            log.error(err)
        return result
