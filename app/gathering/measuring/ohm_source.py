'''
    This module is pretty experimental and uses pythonnet to laod a C#-DLL
    The OpenHardwareMonitrLib is part of a great Windows software that has
    a lot of hardware monitoring.

    It maps the Hardware and Sensors concept from the OHMLib onto the components/metrics system
'''

from misc.helper import importIfExists
from misc.constants import Operating_System
from gathering.measuring.MeasuringSource import MeasuringSource
import logging

log = logging.getLogger("opserv.gathering.ohm")
log.setLevel(logging.DEBUG)

import sys
import time
import os
import atexit

# These type definitions come directly from the OHM source
sensor_types = [
    "Voltage", #V
    "Clock", # MHz
    "Temperature", # °C
    "Load", # %
    "Fan", # RPM
    "Flow", # L/h
    "Control", # %
    "Level", # %
    "Factor", # 1
    "Power", # W
    "Data", # GB = 2^30 Bytes
]

hardware_type =  [
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

tempList = []


sys.path.append("C:/Users/Alex/Dropbox/Schule/Semester 5/Studienarbeit 2/Source/opserv-backend/app/extern_dependency")
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
    memory_data = {}
    disk_list = []

    def __init__(self):
        self.init()

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

        self.clr = importIfExists("clr")

        if not self.clr:
            return
        try:
            self.clr.AddReference("OpenHardwareMonitorLib")
        except Exception as err:
            log.error(err)
            log.error("Error during addReference to the OHM Lib")
            return
        try:
            from OpenHardwareMonitor import Hardware
        except Exception as err:
            log.error(err)
            log.error("Error during importing of hardware class from OHM Lib")
            return
        # Open PC Connection
        self.hardware_class = Hardware
        self.pc = Hardware.Computer()

        self.pc.MotherboardEnabled = True
        self.pc.RAMEnabled = True
        self.pc.GPUEnabled = True
        self.pc.CPUEnabled = True
        self.pc.HDDEnabled = True
        # Set Handlers

        self.pc.HardwareAdded += self.ohm_hardware_added_handler
        self.pc.HardwareRemoved += self.ohm_hardware_removed_handler

        self.pc.Open()
        self._init_complete = True
        pass

    def deinit(self):
        '''
            De-Initializes the measuring source, removing connections etc.
            Returns True if deinit was successfull, False if it errord
        '''
        self.pc.Close()
        self._init_complete = False
        # Close PC connection

        pass

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
        if component == "core":
            result = self.get_core_measurement(metric, args)
        elif component == "gpu":
            result = self.get_gpu_measurement(metric, args)
        elif component == "memory":
            result = self.get_memory_measurement(metric, args)
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
        log.info(hardware_type[hardware.get_HardwareType()])
        log.info(hardware.active)
        log.info(hardware.settings)
        current_hw = hardware_type[hardware.get_HardwareType()]
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

        #self.hardware.append(hardware)

        for hw in hardware.SubHardware:
            self.ohm_hardware_added_handler(hw)
    def ohm_hardware_removed_handler(self, hardware):
        """
            Hardware Removal handler for the OHM library
            This is called when a given hardware is disconnected or the 
            Computer object is closed
        """
        log.info("Removing Hardware")
        log.info(type(hardware))
        log.info(hardware.name)
        log.info(hardware_type[hardware.get_HardwareType()])
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
        new_cpu["cores"] = int(hardware.coreCount)
        # Get CPU Name
        new_cpu["info"] = hardware.name

        new_cores = []
        for i in range(new_cpu["cores"]):
            new_cores.append({
                "id" : i + (new_cpu["id"] * new_cpu["cores"]), # Assumes all CPUs have the same corecount
                "info" : "CPU #{0} Core #{1}".format(new_cpu["id"], i)
            })

        # Update the supported_comps dict

        self.add_supported_metric("cpu", "info")
        self.add_supported_metric("core", "info")
        self.add_supported_metric("system", "cpus")
        self.add_supported_metric("system", "cores")


        for sensor in hardware.Sensors:
            sens_type = sensor_types[sensor.SensorType]
            # Get Core Number, value is -1 if its for the cpu package
            sensor_id = parse_cpu_sensor_name(sensor.Name)
            log.info("Got new sensor %s ID: %d, Type: %s", sensor.Name, sensor_id, sens_type)
            if sens_type == "Load":
                if sensor_id == -1:
                    self.add_supported_metric("cpu", "usage")
                    new_cpu["usage_sensor"] = (hardware, sensor)
                else:
                    self.add_supported_metric("core", "usage")
                    new_cores[sensor_id]["usage_sensor"] = (hardware, sensor)
            elif sens_type == "Temperature":
                if sensor_id == -1:
                    self.add_supported_metric("cpu", "temperature")
                    new_cpu["temperature_sensor"] = (hardware, sensor)
                else:
                    self.add_supported_metric("core", "temperature")
                    new_cores[sensor_id]["temperature_sensor"] = (hardware, sensor)
            elif sens_type == "Clock":
                if sensor.Name.find("Bus Speed") != -1:
                    break # Ignore Bus speeds
                if sensor_id == -1:
                    self.add_supported_metric("cpu", "frequency")
                    new_cpu["frequency_sensor"] = (hardware, sensor)
                else:
                    self.add_supported_metric("core", "frequency")
                    new_cores[sensor_id]["frequency_sensor"] = (hardware, sensor)

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
        pass
    def add_disk(self, hardware):
        """
            Sub-Handler to process newly found disks in the system
        """
        pass

    def get_cpu_measurement(self, metric, args):
        """
            Updates the hardware class for the specified cpu (not cores, whole cpu socket)
            and returns the value for the  specified metric
        """
        for cpu in self.cpu_list:
            log.info(cpu)
            if int(cpu["id"]) == int(args):
                if metric == "usage":
                    sensor_type = "usage_sensor"
                elif metric == "frequency":
                    sensor_type = "frequency_sensor"
                elif metric == "temperature":
                    sensor_type = "temperature_sensor"
                cpu[sensor_type][0].Update()
                log.info("Taking measurement, Type: {0}, Value: {1}".format(metric, cpu[sensor_type][1].Value))
                return cpu[sensor_type][1].Value
        raise ValueError("CPU given in args not found! {}".format(args))
    def get_gpu_measurement(self, metric, args):
        """
            Updates the hardware object for the specified GPU and returns the value for metric
        """
        pass
    def get_core_measurement(self, metric, args):
        """
            Updates the hardware of the given cpu core to get a measurement
            for the specified metric
        """
        for core in self.core_list:
            if core["id"] == args:
                if metric == "usage":
                    sensor_type = "usage_sensor"
                elif metric == "frequency":
                    sensor_type = "frequency_sensor"
                elif metric == "temperature":
                    sensor_type = "temperature_sensor"
                core[sensor_type][0].Update()
                log.info("Taking measurement, Type: {0}, Value: {1}".format(metric, core[sensor_type][1].Value))
                return core[sensor_type][1].Value
        raise ValueError("Core given in args not found! {}".format(args))
    def get_disk_measurement(self, metric, args):
        """
            Gets a measurement from the specified disk (not as in partition, but physical disks)
            And returns the value of the specified metric
        """
        pass
    def get_memory_measurement(self, metric, args):
        """
            Updates the memory hardware object and returns the value of the specified metric
        """
        pass
    def get_system_measurement(self, metric):
        """
            Gets the measurement from specified metric for the system component
        """
        if metric == "cpus":
            return list(range(len(self.cpu_list)))
        elif metric == "cores":
            return list(range(len(self.core_list)))

def parse_cpu_sensor_name(name):
    """
        Tries to resolve the Name attribute from the OHM CPU class into a 
        core number or into -1 (which is the whole cpu package)
    """
    num_pos = name.find("#")  + 1
    try:
        core_number = int(name[num_pos:])
        return core_number - 1 # Minus one to make it zero based
    except ValueError as err:
        # Core number cannot be parsed (so it is either total load or not in the name)
        return -1
