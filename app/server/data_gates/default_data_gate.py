import time
from collections import Iterable

from database.unified_database_interface import UnifiedDatabaseInterface
from misc import data_manager
from server.data_gates.outbound_gate_interface import OutboundGateInterface


class DefaultDataGate(OutboundGateInterface):
    @classmethod
    def get_valid_arguments(cls, component: str) -> Iterable:
        # TODO Improve readability
        last_saved_measurement = data_manager.get_measurement(component="system", metric=component)

        present_arguments = []
        if last_saved_measurement is not None and 'value' in last_saved_measurement:
            present_arguments = last_saved_measurement['value']

        persisted_arguments = UnifiedDatabaseInterface.get_component_metrics_writer_reader().get_component_args(
            component)

        # TODO url encode every value
        return cls.__merge_two_lists(
            present_arguments,
            persisted_arguments
        )

    @classmethod
    def is_argument_valid(cls, argument: str, component: str) -> bool:
        if argument is None or component is None:
            return False

        return argument in cls.get_valid_arguments(component)

    @classmethod
    def get_measurements(cls, component: str, metric: str, argument: str = None, start_time: int = 0,
                         end_time: int = time.time() * 1000, limit: int = 5000) -> Iterable:
        # TODO url decode every value

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
    def get_last_measurement(cls, component: str, metric: str, argument: str = None) -> dict:
        # TODO url decode every value

        if component is None or metric is None:
            return None

        return data_manager.get_measurement(component, metric, argument)

    @classmethod
    def get_gathering_rate(cls, component: str, metric: str, argument: str = None) -> int:
        # TODO url decode every value

        # TODO Implement method
        return 0

    @classmethod
    def set_gathering_rate(cls, component: str, metric: str, gathering_rate: int, argument: str = None) -> None:
        # TODO url decode every value

        # TODO Implement method
        return None

    @classmethod
    def get_user_preference(cls, key: str) -> str:
        # TODO url decode every value

        if key is None:
            return None

        return UnifiedDatabaseInterface.get_user_preferences_writer_reader().get_user_preference(key)

    @classmethod
    def set_user_preference(cls, key: str, value: str) -> None:
        # TODO url decode every value

        if key is not None:
            UnifiedDatabaseInterface.get_user_preferences_writer_reader().set_user_preference(key, value)

    # TODO Is this the right place for this? -> Extract to some helper interface
    @classmethod
    def __merge_two_lists(cls, first_list, second_list):
        def __stringify_list(raw_list) -> list:
            return list(
                map(str, raw_list)
            )

        first_list = __stringify_list(first_list)
        second_list = __stringify_list(second_list)

        return first_list + list(set(second_list) - set(first_list))
