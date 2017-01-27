import time
from urllib.parse import unquote_plus, quote_plus

from database.unified_database_interface import UnifiedDatabaseInterface
from misc import data_manager
from misc import queue_manager
from server.data_gates.outbound_gate_interface import OutboundGateInterface


class DefaultDataGate(OutboundGateInterface):
    @classmethod
    def get_valid_arguments(cls, component_type: str) -> list:
        # TODO Improve readability
        last_saved_measurement = data_manager.get_measurement(component="system", metric=component_type)

        present_arguments = []
        if last_saved_measurement is not None and 'value' in last_saved_measurement:
            present_arguments = last_saved_measurement['value']

        persisted_arguments = UnifiedDatabaseInterface.get_component_metrics_writer_reader().get_component_args(
            component_type)

        all_arguments = cls.__merge_two_lists(
            present_arguments,
            persisted_arguments
        )

        return list(
            map(
                cls.double_encode_argument,
                all_arguments
            )
        )

    @classmethod
    def is_argument_valid(cls, argument: str, component: str) -> bool:
        if argument is None or component is None:
            return False

        # For some reason, python decodes the url already once, which results in error in cases of an encoded slash '/'
        # thus arguments have to be double encoded to prevent this. They have to be decoded once back to original input.
        valid_arguments = map(
            cls.decode_argument,
            cls.get_valid_arguments(component)
        )

        return argument in valid_arguments

    @classmethod
    def get_measurements(cls, component_type: str, component_arg: str, metric: str, start_time: int,
                         end_time: int, limit: int) -> list:
        measurement_data_reader = UnifiedDatabaseInterface.get_measurement_data_reader()

        component_type = cls.decode_argument(component_type)
        metric = cls.decode_argument(metric)
        component_arg = cls.decode_argument(component_arg)

        if component_type is None or metric is None:
            raise TypeError("Both component_type and metric have to be valid string objects.")

        if start_time is None:
            start_time = measurement_data_reader.get_timestamp_of_first_measurement(component_type, component_arg,
                                                                                    metric)

        if end_time is None:
            end_time = int(time.time() * 1000)

        if limit is None:
            limit = 100

        raw_measurements = measurement_data_reader.get_min_avg_max(
            component_type, component_arg, metric, start_time, end_time, limit
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
    def get_last_measurement(cls, component_type: str, metric: str, component_arg: str = None) -> dict:
        component_type = cls.decode_argument(component_type)
        metric = cls.decode_argument(metric)
        component_arg = cls.decode_argument(component_arg)

        if component_type is None or metric is None:
            raise TypeError("Both component_type and metric have to be valid string objects.")

        return data_manager.get_measurement(component_type, metric, component_arg)

    @classmethod
    def get_gathering_rate(cls, component: str, metric: str, argument: str = None) -> int:
        component = cls.decode_argument(component)
        metric = cls.decode_argument(metric)
        argument = cls.decode_argument(argument)

        return UnifiedDatabaseInterface.get_component_metrics_writer_reader().get_gathering_rate(
            component,
            argument,
            metric
        )

    @classmethod
    def set_gathering_rate(cls, component: str, metric: str, gathering_rate: int, argument: str = None) -> None:
        component = cls.decode_argument(component)
        metric = cls.decode_argument(metric)
        argument = cls.decode_argument(argument)

        UnifiedDatabaseInterface.get_component_metrics_writer_reader().set_gathering_rate(
            component,
            argument,
            metric,
            gathering_rate
        )

        queue_manager.set_gathering_rate(
            component,
            metric,
            gathering_rate,
            argument
        )

    @classmethod
    def get_user_preference(cls, key: str) -> str:
        key = cls.decode_argument(key)

        if key is None:
            return None

        return UnifiedDatabaseInterface.get_user_preferences_writer_reader().get_user_preference(key)

    @classmethod
    def set_user_preference(cls, key: str, value: str) -> None:
        key = cls.decode_argument(key)

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

    @classmethod
    def double_encode_argument(cls, argument) -> str:
        if argument is None:
            return None

        return quote_plus(quote_plus(argument))

    @classmethod
    def decode_argument(cls, argument) -> str:
        if argument is None:
            return None

        return unquote_plus(argument)
