import time

from database.unified_database_interface import UnifiedDatabaseInterface
from misc import data_manager
from misc import queue_manager
from misc.constants import COMPS_TO_SYSTEM_METRICS
from server.data_gates.outbound_gate_interface import OutboundGateInterface
from misc.standalone_helper import merge_n_lists


class DefaultDataGate(OutboundGateInterface):
    @classmethod
    def get_valid_arguments(cls, component_type: str) -> list:
        if component_type is None:
            raise TypeError("component_type has to be a valid string object.")

        cached_arguments = cls.__get_cached_arguments(component_type)

        persisted_arguments = UnifiedDatabaseInterface.get_component_metrics_writer_reader().get_component_args(
            component_type
        )

        return merge_n_lists(cached_arguments, persisted_arguments)

    @classmethod
    def __get_cached_arguments(cls, component_type) -> list:
        system_metric = COMPS_TO_SYSTEM_METRICS(component_type)

        if system_metric is not None:
            system_arg_measurement = data_manager.get_measurement(component="system", metric=system_metric)

            if system_arg_measurement is not None and 'value' in system_arg_measurement:
                return system_arg_measurement['value']
        return []

    @classmethod
    def is_argument_valid(cls, component_type: str, component_arg: str) -> bool:
        if component_arg is None or component_type is None:
            return False
        return component_arg in cls.get_valid_arguments(component_type)

    @classmethod
    def get_measurements(cls, component_type: str, component_arg: str, metric: str, start_time: int,
                         end_time: int, limit: int) -> list:
        measurement_data_reader = UnifiedDatabaseInterface.get_measurement_data_reader()

        if component_type is None or metric is None:
            raise TypeError("Both component_type and metric have to be valid string objects.")

        if start_time is None:
            start_time = measurement_data_reader.get_timestamp_of_first_measurement(component_type, component_arg,
                                                                                    metric)

        if end_time is None:
            end_time = int(time.time() * 1000)

        if limit is None:
            limit = 100

        raw_measurements = measurement_data_reader.get_condensed_data(
            component_type, component_arg, metric, start_time, end_time, limit
        )

        return list(
            map(
                lambda item: {
                    "min": item[1],
                    "avg": item[2],
                    "max": item[3],
                    "timestamp": item[0]
                }, raw_measurements)
        )

    @classmethod
    def get_last_measurement(cls, component_type: str, component_arg: str, metric: str) -> dict:
        if component_type is None or metric is None:
            raise TypeError("Both component_type and metric have to be valid string objects.")

        return data_manager.get_measurement(component_type, metric, component_arg)

    @classmethod
    def get_gathering_rate(cls, component_type: str, component_arg: str, metric: str) -> int:
        if component_type is None or metric is None:
            raise TypeError("Both component_type and metric have to be valid string objects.")

        return UnifiedDatabaseInterface.get_component_metrics_writer_reader().get_gathering_rate(
            component_type,
            component_arg,
            metric
        )

    @classmethod
    def get_gathering_rates(cls) -> list:
        pass

    @classmethod
    def set_gathering_rate(cls, component_type: str, component_arg: str, metric: str, gathering_rate: int) -> None:
        UnifiedDatabaseInterface.get_component_metrics_writer_reader().set_gathering_rate(
            component_type,
            component_arg,
            metric,
            gathering_rate
        )

        queue_manager.set_gathering_rate(
            component_type,
            metric,
            gathering_rate,
            component_arg
        )

    @classmethod
    def delete_gathering_rate(cls, component_type: str, component_arg: str, metric: str) -> None:
        pass

    @classmethod
    def get_user_preference(cls, key: str) -> str:
        if key is None:
            return None

        return UnifiedDatabaseInterface.get_user_preferences_writer_reader().get_user_preference(key)

    @classmethod
    def set_user_preference(cls, key: str, value: str) -> None:
        if key is not None:
            UnifiedDatabaseInterface.get_user_preferences_writer_reader().set_user_preference(key, value)

    @classmethod
    def delete_user_preference(cls, key: str) -> None:
        if key is not None:
            UnifiedDatabaseInterface.get_user_preferences_writer_reader().delete_user_preference(key)
