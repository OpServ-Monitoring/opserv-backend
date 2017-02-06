"""

    Gets Measurements from the appropriate sources
    Is also responsible for sending the data to the
    queue and data manager and caching db values
    until a threshold(count or time) has been reached
"""
import logging
import time

import misc.data_manager as data_manager
import misc.queue_manager as queue_manager
from database.unified_database_interface import UnifiedDatabaseInterface
from gathering.measuring.cpuinfo_source import PyCpuInfoSource
from gathering.measuring.null_source import NullSource
from gathering.measuring.ohm_source import OHMSource
from gathering.measuring.psutil_source import PsUtilWrap
from gathering.measuring.pyspectator_source import PySpectatorSource
from gathering.measuring.raspi_temp_source import RaspiTempSource

log = logging.getLogger("opserv." + __name__)

transaction = UnifiedDatabaseInterface.get_measurement_insertion_transaction()


class MeasurementManager():
    measuring_sources = []

    @classmethod
    def init_manager(cls):
        '''
            Initializes the measurement manager by importing and initializing
            all the measuring sources and appending them to the list
        '''
        # Get all the available Measuring Sources
        cls.measuring_sources.append(PsUtilWrap())
        cls.measuring_sources.append(OHMSource())
        cls.measuring_sources.append(PyCpuInfoSource())
        cls.measuring_sources.append(PySpectatorSource())
        cls.measuring_sources.append(RaspiTempSource())
        cls.measuring_sources.append(NullSource())

    @classmethod
    def make_measurement(cls, component, metric, args):
        '''
            Makes a proper measurement by first taking the measurement and then
            inserting it into the data and queue manager aswell as into the database
            Before the insertion the data is validated
        '''
        # First a measurement has to be taken
        new_measurement = cls.get_measurement(component, metric, args)

        # Validate the measurement
        if not cls.measurement_is_valid(new_measurement):
            log.error("Measurement taken was not valid %s:%s, %s, %s",
                      new_measurement, component, metric, args)
            return

        # Put that data into the queue
        queue_manager.put_measurement_into_queue(component, metric, new_measurement, args)

        # Update the data in the realtime dictionary
        data_manager.set_measurement(component, metric, new_measurement, args)

        # And lastly add it to the commitlist for the database TODO
        cls.save_to_database(new_measurement, component, metric, args)

    @classmethod
    def save_to_database(cls, measurement, component, metric, args):
        '''
            Saves the given measurement to the database or enqueues it to be saved
            at a later time to avoid too much commits and DB hogging
        '''
        transaction.insert_measurement(component, args, metric, measurement["timestamp"],
                                       str(measurement["value"]))
        transaction.commit_transaction()

    @classmethod
    def measurement_is_valid(cls, measure_to_check):
        '''
            Checks the given measurement for validity
        '''
        # TODO add more elaborate validaiton
        if measure_to_check is None:
            return False
        return True

    @classmethod
    def get_measurement(cls, component, metric, args):
        """
            Given the component and metric this function uses the libraries to make a measurement
            Returns: The value of the measurement
        """
        # Lowercase to avoid any case errors
        component = component.lower()
        metric = metric.lower()

        measured_value = None
        for src in cls.measuring_sources:
            if src.can_measure(component, metric):
                try:
                    measured_value = src.get_measurement(component, metric, args)
                    if measured_value is not None:
                        break  # Just use the first src that is able to measure
                except Exception as err:
                    log.error(err)
                    log.error("Measuring failed here %s, %s, %s, %s",
                              component, metric, args, str(src))

        if measured_value is not None:
            log.debug("Gathered {0} from {1},{2},{3}".format(measured_value,
                                                             component, metric, args))
            return {
                "timestamp": time.time() * 1000,
                "value": measured_value
            }

        log.error("Tried to get unimplemented component")
        return None
