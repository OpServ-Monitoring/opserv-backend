import time
from urllib.parse import unquote_plus, quote_plus

from database.unified_database_interface import UnifiedDatabaseInterface
from misc import data_manager
from misc import queue_manager
from misc.constants import COMPS_TO_SYSTEM_METRICS
from server.data_gates.outbound_gate_interface import OutboundGateInterface


class DefaultDataGate(OutboundGateInterface):

    @classmethod
    def get_valid_arguments(cls, component_type: str) -> list:
        cached_arguments = cls.__get_cached_arguments(component_type)

        persisted_arguments = UnifiedDatabaseInterface.get_component_metrics_writer_reader().get_component_args(
            component_type
        )

        return cls.__merge_two_lists(
            cached_arguments,
            persisted_arguments
        )

    @classmethod
    def __get_cached_arguments(cls, component_type):
        system_metric = COMPS_TO_SYSTEM_METRICS(component_type)

        if system_metric is not None:
            system_arg_measurement = data_manager.get_measurement(component="system", metric=system_metric)

            if system_arg_measurement is not None and 'value' in system_arg_measurement:
                return system_arg_measurement['value']
        return []

    # TODO Make sure every argument passed here is decoded already (on the http api side)
    @classmethod
    def is_argument_valid(cls, component_arg: str, component_type: str) -> bool:
        if component_arg is None or component_type is None:
            return False
        return component_arg in cls.get_valid_arguments(component_type)

    @classmethod
    def get_measurements(cls, component_type: str, component_arg: str, metric: str, start_time: int,
                         end_time: int, limit: int) -> list:
        measurement_data_reader = UnifiedDatabaseInterface.get_measurement_data_reader()

        # TODO Remove decoding, shouldn't be part of data provisioning (e.g. websocket may not need encoded args)
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
    def get_last_measurement(cls, component_type: str, metric: str, component_arg: str = None) -> dict:
        # TODO Remove decoding, shouldn't be part of data provisioning (e.g. websocket may not need encoded args)
        component_type = cls.decode_argument(component_type)
        metric = cls.decode_argument(metric)
        component_arg = cls.decode_argument(component_arg)

        if component_type is None or metric is None:
            raise TypeError("Both component_type and metric have to be valid string objects.")

        return data_manager.get_measurement(component_type, metric, component_arg)

    @classmethod
    def get_gathering_rate(cls, component: str, metric: str, argument: str = None) -> int:
        # TODO Remove decoding, shouldn't be part of data provisioning (e.g. websocket may not need encoded args)

        component = cls.decode_argument(component)
        metric = cls.decode_argument(metric)
        argument = cls.decode_argument(argument)

        return UnifiedDatabaseInterface.get_component_metrics_writer_reader().get_gathering_rate(
            component,
            argument,
            metric
        )

    @classmethod
    def get_gathering_rates(cls) -> list:
        pass

    @classmethod
    def set_gathering_rate(cls, component: str, metric: str, gathering_rate: int, argument: str = None) -> None:
        # TODO Remove decoding, shouldn't be part of data provisioning (e.g. websocket may not need encoded args)

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
    def delete_gathering_rate(cls, component: str, metric: str, argument: str = None) -> None:
        pass

    @classmethod
    def get_user_preference(cls, key: str) -> str:
        # TODO Remove decoding, shouldn't be part of data provisioning (e.g. websocket may not need encoded args)

        key = cls.decode_argument(key)

        if key is None:
            return None

        return UnifiedDatabaseInterface.get_user_preferences_writer_reader().get_user_preference(key)

    @classmethod
    def set_user_preference(cls, key: str, value: str) -> None:
        # TODO Remove decoding, shouldn't be part of data provisioning (e.g. websocket may not need encoded args)

        key = cls.decode_argument(key)

        if key is not None:
            UnifiedDatabaseInterface.get_user_preferences_writer_reader().set_user_preference(key, value)

    @classmethod
    def delete_user_preference(cls, key: str) -> None:
        pass

    # TODO Extract this to some helper interface
    @classmethod
    def __merge_two_lists(cls, first_list, second_list):
        def __stringify_list(raw_list) -> list:
            return list(
                map(str, raw_list)
            )

        first_list = __stringify_list(first_list)
        second_list = __stringify_list(second_list)

        return first_list + list(set(second_list) - set(first_list))

    # TODO Extract this somewhere, encoding should not be part of the data gate but the HTTP API instead
    @classmethod
    def double_encode_argument(cls, argument) -> str:
        if argument is None:
            return None

        return quote_plus(quote_plus(argument))

    # TODO Extract this somewhere, encoding should not be part of the data gate but the HTTP API instead
    @classmethod
    def decode_argument(cls, argument) -> str:
        if argument is None:
            return None

        return unquote_plus(argument)
