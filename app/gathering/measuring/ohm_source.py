'''
    This module is pretty experimental and uses pythonnet to laod a C#-DLL
    The OpenHardwareMonitorLib is a pretty sophisticated library to get system metrics
    For more information about the project/code visit the GitHub Repository
    https://github.com/openhardwaremonitor/openhardwaremonitor
    
    It maps the Hardware and Sensors concept from the OHMLib onto the components/metrics system
'''

import atexit
import logging
import os
import sys

from gathering.measuring.MeasuringSource import MeasuringSource
from misc.constants import Operating_System
from misc.helper import import_if_exists, get_path_to_app

log = logging.getLogger("opserv.gathering.ohm")
log.setLevel(logging.DEBUG)

# These type definitions come directly from the OHM source
SENSORTYPES = [
    "Voltage",  # V
    "Clock",  # MHz
    "Temperature",  # °C
    "Load",  # %
    "Fan",  # RPM
    "Flow",  # L/h
    "Control",  # %
    "Level",  # %
    "Factor",  # 1
    "Power",  # W
    "Data",  # GB = 2^30 Bytes
]

# Map sensor types to dict keys
# These two dicts are necessary to bind the opserv component system to the OHM hardware/sensors
TYPE_MAP = {
    "Load": ("usage", "usage_sensor"),
    "Temperature": ("temperature", "temperature_sensor"),
    "Clock": ("frequency", "frequency_sensor")
}

TYPE_MAP_REVERSE = {
    "usage": ("Load", "usage_sensor"),
    "frequency": ("Clock", "frequency_sensor"),
    "temperature": ("Temperature", "temperature_sensor")
}

HARDWARETYPES = [
    "Mainboard",
    "SuperIO",
    "CPU",
    "RAM",
    "GpuNvidia",
    "GpuAti",
    "TBalancer",
    "Heatmaster",
    "HDD"
]

# Append DLL path to the sys path array
sys.path.append(os.path.join(get_path_to_app(), "extern_dependency"))


class OHMSource(MeasuringSource):
    '''
        Source description
    '''

    _supported_os = [Operating_System.windows]
    _supported_comps = {

    }

    cpu_list = []
    core_list = []
    gpu_list = []
    memory_data = None
    disk_list = []

    def __init__(self):
        self.clr = None
        self.hardware = []
        self._init_complete = False

        atexit.register(self.deinit)

        self.init()

    def init(self):
        '''
            Initializes the measuring source (opening hardware connections etc.)
            If initialization is successful, it will return True
            If errors occured, the return value will be False
        '''

        self.clr = import_if_exists("clr")

        if not self.clr:
            return
        try:
            self.clr.AddReference("OpenHardwareMonitorLib")
        except Exception as err:
            log.error(err)
            log.error("Error during addReference to the OHM Lib")
            return
        try:
            # Ignore PyLint error since this module is being loaded at runtime
            from OpenHardwareMonitor import Hardware  # pylint: disable=E0401
        except Exception as err:
            log.error(err)
            log.error("Error during importing of hardware class from OHM Lib")
            return
        # Open PC Connection
        self.hardware_class = Hardware
        self.computer = Hardware.Computer()

        self.computer.MotherboardEnabled = True
        self.computer.RAMEnabled = True
        self.computer.GPUEnabled = True
        self.computer.CPUEnabled = True
        self.computer.HDDEnabled = True
        # Set Handlers

        self.computer.HardwareAdded += self.ohm_hardware_added_handler
        self.computer.HardwareRemoved += self.ohm_hardware_removed_handler

        self.computer.Open()
        self._init_complete = True

    def deinit(self):
        '''
            De-Initializes the measuring source, removing connections etc.
            Returns True if deinit was successfull, False if it errord
        '''
        if self._init_complete:
            self.computer.Close()
            self._init_complete = False

    def get_measurement(self, component, metric, args):
        '''
            Retrieves a measurement from the measuring source
            given the component, metric and optionally arguments
        '''
        if not self._init_complete:
            raise ValueError("MeasuringSource is not initialized")

        result = None
        if component == "cpu":
            result = self.get_cpu_measurement(metric, args)
        if component == "cpucore":
            result = self.get_core_measurement(metric, args)
        elif component == "gpu":
            result = self.get_gpu_measurement(metric, args)
        elif component == "memory":
            result = self.get_memory_measurement(metric)
        elif component == "disk":
            result = self.get_disk_measurement(metric, args)
        elif component == "system":
            result = self.get_system_measurement(metric)
        return result

    def ohm_hardware_added_handler(self, hardware):
        """
            Hardware Added Handler
            This is called with the given hardware when a new hardware on the computer is found
        """
        log.info("Adding Hardware")
        log.info(type(hardware))
        log.info(hardware.name)
        log.info(HARDWARETYPES[hardware.get_HardwareType()])
        log.info(hardware.active)
        log.info(hardware.settings)
        current_hw = HARDWARETYPES[hardware.get_HardwareType()]
        if current_hw == "CPU":
            log.info("Found a CPU %s", hardware.name)
            self.add_cpu(hardware)
        elif current_hw == "GpuNvidia" or current_hw == "GpuAti":
            log.info("Found a GPU %s", hardware.name)
            self.add_gpu(hardware)
        elif current_hw == "RAM":
            log.info("Found a RAM %s", hardware.name)
            self.add_memory(hardware)
        elif current_hw == "HDD":
            log.info("Found an HDD %s", hardware.name)
            self.add_disk(hardware)

        for sub_hw in hardware.SubHardware:
            self.ohm_hardware_added_handler(sub_hw)

    def ohm_hardware_removed_handler(self, hardware):
        """
            Hardware Removal handler for the OHM library
            This is called when a given hardware is disconnected or the
            Computer object is closed
        """
        log.info("Removing Hardware")
        log.info(type(hardware))
        log.info(hardware.name)
        log.info(HARDWARETYPES[hardware.get_HardwareType()])
        log.info(hardware.active)
        log.info(hardware.settings)

    def add_cpu(self, hardware):
        '''
            Adds the given CPU (as OHM Hardware Object) to the cpu list
            Also adds all its cores and updates the supported metrics
        '''
        # sensor.Index does not represent the core number
        # It has to be parsed from the sensor name


        # First check whether the processor is already added
        for cpu in self.cpu_list:
            if cpu["id"] == hardware.processorIndex:
                return

        new_cpu = {}

        # Get CPU Index
        log.info("Processor Index: %d", hardware.processorIndex)
        new_cpu["id"] = int(hardware.processorIndex)
        # Get CPU Cores
        log.info("Core Count: %d", hardware.coreCount)
        new_cpu["cpucores"] = int(hardware.coreCount)
        # Get CPU Name
        new_cpu["info"] = hardware.name

        new_cores = []
        for i in range(new_cpu["cpucores"]):
            new_cores.append({
                # Assumes all CPUs have the same corecount
                "id": i + (new_cpu["id"] * new_cpu["cpucores"]),
                "info": "CPU #{0} Core #{1}".format(new_cpu["id"], i)
            })

        # Update the supported_comps dict

        self.add_supported_metric("cpu", "info")
        self.add_supported_metric("cpucore", "info")
        self.add_supported_metric("system", "cpus")
        self.add_supported_metric("system", "cpucores")

        for sensor in hardware.Sensors:
            sens_type = SENSORTYPES[sensor.SensorType]
            # Get Core Number, value is -1 if its for the cpu package
            sensor_id = parse_cpu_sensor_name(sensor.Name)
            log.info("Got new sensor %s ID: %d, Type: %s", sensor.Name, sensor_id, sens_type)

            # Ignore Bus Speed
            if sensor.Name.find("Bus Speed") != -1:
                break
            if sens_type in TYPE_MAP:
                if sensor_id == -1:
                    self.add_supported_metric("cpu", TYPE_MAP[sens_type][0])
                    new_cpu[TYPE_MAP[sens_type][1]] = (hardware, sensor)
                else:
                    self.add_supported_metric("cpucore", TYPE_MAP[sens_type][0])
                    new_cores[sensor_id][TYPE_MAP[sens_type][1]] = (hardware, sensor)

        # Add the newly found CPU and its cores into the lists
        self.cpu_list.append(new_cpu)
        self.core_list.extend(new_cores)

    def add_gpu(self, hardware):
        """
            Sub-Handler to process GPUs in the system
        """
        pass

    def add_memory(self, hardware):
        """
            Sub-Handler to process memory in the system
        """
        log.info("Got a new RAM hardware")
        self.add_supported_metric("memory", "free")
        self.add_supported_metric("memory", "used")
        self.add_supported_metric("memory", "total")
        self.memory_data = hardware

    def add_disk(self, hardware):
        """
            Sub-Handler to process newly found disks in the system
        """

        # Currently Deactivated since there is no easy way to uniquely identify disks
        return

        self.add_supported_metric("disk", "info")
        self.add_supported_metric("system", "disks")
        log.info(hardware)
        log.info(hardware.name)
        log.info(hardware.GetReport())
        for smart in hardware.SmartAttributes:
            log.info(smart.Name)
        for sensor in hardware.Sensors:
            if str(sensor.Name) == "Used Space":
                self.add_supported_metric("disk", "usage")
            log.info(sensor)
            log.info(sensor.Name)
            log.info(sensor.SensorType)
        pass

    def get_cpu_measurement(self, metric, args):
        """
            Updates the hardware class for the specified cpu (not cores, whole cpu socket)
            and returns the value for the  specified metric
        """
        for cpu in self.cpu_list:
            log.info(cpu)
            if int(cpu["id"]) == int(args):
                if metric in TYPE_MAP_REVERSE:
                    sens_type = TYPE_MAP_REVERSE[metric][1]
                    cpu[sens_type][0].Update()
                    log.info("Taking measurement, Type: %s, Value: %f",
                             metric, cpu[sens_type][1].Value)
                    return cpu[sens_type][1].Value
                elif metric == "info":
                    return cpu["info"]
        raise ValueError("CPU given in args not found! {}".format(args))

    def get_core_measurement(self, metric, args):
        """
            Updates the hardware of the given cpu core to get a measurement
            for the specified metric
        """
        args = int(args)
        for core in self.core_list:
            if core["id"] == args:
                if metric in TYPE_MAP_REVERSE:
                    sens_type = TYPE_MAP_REVERSE[metric][1]
                    core[sens_type][0].Update()
                    log.info("Taking measurement, Type: %s, Value: %s",
                             metric, str(core[sens_type][1].Value))
                    return core[sens_type][1].Value
        raise ValueError("Core given in args not found! {}".format(args))

    def get_gpu_measurement(self, metric, args):
        """
            Updates the hardware object for the specified GPU and returns the value for metric
        """
        pass

    def get_disk_measurement(self, metric, args):
        """
            Gets a measurement from the specified disk (not as in partition, but physical disks)
            And returns the value of the specified metric
        """
        pass

    def get_memory_measurement(self, metric):
        """
            Updates the memory hardware object and returns the value of the specified metric
        """
        self.memory_data.Update()
        byte_multiplier = 1024 * 1024 * 1024
        if metric == "free":
            return self.memory_data.availableMemory.Value * byte_multiplier
        elif metric == "used":
            return self.memory_data.usedMemory.Value * byte_multiplier
        elif metric == "total":
            return (self.memory_data.usedMemory.Value
                    + self.memory_data.availableMemory.Value) * byte_multiplier

    def get_system_measurement(self, metric):
        """
            Gets the measurement from specified metric for the system component
        """
        if metric == "cpus":
            return list(range(len(self.cpu_list)))
        elif metric == "cpucores":
            return list(range(len(self.core_list)))


def parse_cpu_sensor_name(name):
    """
        Tries to resolve the Name attribute from the OHM CPU class into a
        core number or into -1 (which is the whole cpu package)
    """
    num_pos = name.find("#") + 1
    try:
        core_number = int(name[num_pos:])
        return core_number - 1  # Minus one to make it zero based
    except ValueError:
        # Core number cannot be parsed (so it is either total load or not in the name)
        return -1
