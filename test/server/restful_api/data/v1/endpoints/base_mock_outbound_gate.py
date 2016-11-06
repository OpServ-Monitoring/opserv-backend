from collections import Iterable

import time

from server.data_gates.outbound_gate_interface import OutboundGateInterface


class BaseMockOutboundGate(OutboundGateInterface):
    @classmethod
    def get_last_measurement(cls, component: str, metric: str, argument: str = None) -> dict:
        return {
            "value": "75 percent",
            "timestamp": 1234567
        }

    @classmethod
    def is_argument_valid(cls, argument: str, component: str) -> bool:
        return argument in BaseMockOutboundGate.get_valid_arguments(component)

    @classmethod
    def get_valid_arguments(cls, component: str) -> Iterable:
        return [
            "id",
            "2"
        ]

    @classmethod
    def get_user_preference(cls, key: str) -> str:
        pass

    @classmethod
    def get_measurements(cls, component: str, metric: str, argument: str = None, start_time: int = 0,
                         end_time: int = time.time() * 1000, limit: int = 5000) -> Iterable:
        pass

    @classmethod
    def set_user_preference(cls, key: str, value: str) -> None:
        pass

    @classmethod
    def set_gathering_rate(cls, component: str, metric: str, gathering_rate: int, argument: str = None) -> None:
        pass

    @classmethod
    def get_gathering_rate(cls, component: str, metric: str, argument: str = None) -> int:
        pass