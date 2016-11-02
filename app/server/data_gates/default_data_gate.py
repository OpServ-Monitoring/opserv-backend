import time
from collections import Iterable

from database.unified_database_interface import UnifiedDatabaseInterface
from misc import data_manager as DataManager
from server.data_gates.data_gate_interface import DataGateInterface


class DefaultDataGate(DataGateInterface):
    @classmethod
    def get_valid_arguments(cls, component: str) -> Iterable:
        # TODO Improve readability
        last_saved_measurement = DataManager.get_measurement(component="system", metric=component)["value"]

        present_arguments = []
        if last_saved_measurement is not None and 'value' in last_saved_measurement:
            present_arguments = last_saved_measurement['value']

        persisted_arguments = UnifiedDatabaseInterface.get_component_metrics_writer_reader().get_component_args(component)

        return cls.__merge_two_lists(
            cls.__stringify_list(present_arguments),
            cls.__stringify_list(persisted_arguments)
        )

    @classmethod
    def is_argument_valid(cls, argument: str, component: str) -> bool:
        if argument is None or component is None:
            return False

        return argument in cls.get_valid_arguments(component)

    @classmethod
    def get_measurements(cls, component: str, metric: str, argument: str = None, start_time: int = 0,
                         end_time: int = time.time() * 1000, limit: int = 5000) -> str:
        raw_measurements = UnifiedDatabaseInterface.get_measurement_data_reader().get_min_avg_max(
            component, argument, metric, start_time, end_time, limit
        )

        return list(
            map(
                lambda item: {
                    "min": item[4],
                    "avg": item[5],
                    "max": item[6],
                    "timestamp": item[3]
                }, raw_measurements)
        )

    @classmethod
    def get_last_measurement(cls, component: str, metric: str, argument: str = None) -> str:
        if component is None or metric is None:
            return None

        return DataManager.get_measurement(component, metric, argument)

    @classmethod
    def get_gathering_rate(cls, component: str, metric: str, argument: str = None) -> int:
        # TODO Implement method
        pass

    @classmethod
    def set_gathering_rate(cls, component: str, metric: str, gathering_rate: int, argument: str = None) -> None:
        # TODO Implement method
        pass

    # TODO Is this the right place for this? -> Extract to some helper interface
    @classmethod
    def __stringify_list(cls, raw_list) -> list:
        return list(
            map(str, raw_list)
        )

    # TODO Is this the right place for this? -> Extract to some helper interface
    @classmethod
    def __merge_two_lists(cls, first_list, second_list):
        return first_list + list(set(second_list) - set(first_list))
        # TODO Fix error that occurs when value is the same but of different type, e.g. '0' and 0
