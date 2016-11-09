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
        print("is arg valid", argument in BaseMockOutboundGate.get_valid_arguments(component))

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
        return [
            {
                "min": "0 percent",
                "avg": "5 percent",
                "max": "10 percent",
                "timestamp": 1000000
            },
            {
                "min": "10 percent",
                "avg": "15 percent",
                "max": "20 percent",
                "timestamp": 1001000
            },
            {
                "min": "20 percent",
                "avg": "25 percent",
                "max": "30 percent",
                "timestamp": 1002000
            },
            {
                "min": "30 percent",
                "avg": "35 percent",
                "max": "40 percent",
                "timestamp": 1003000
            },
            {
                "min": "40 percent",
                "avg": "45 percent",
                "max": "50 percent",
                "timestamp": 1004000
            },
            {
                "min": "50 percent",
                "avg": "55 percent",
                "max": "60 percent",
                "timestamp": 1005000
            },
            {
                "min": "60 percent",
                "avg": "65 percent",
                "max": "70 percent",
                "timestamp": 1006000
            },
            {
                "min": "70 percent",
                "avg": "75 percent",
                "max": "80 percent",
                "timestamp": 1007000
            },
            {
                "min": "80 percent",
                "avg": "885 percent",
                "max": "90 percent",
                "timestamp": 1008000
            },
            {
                "min": "90 percent",
                "avg": "95 percent",
                "max": "100 percent",
                "timestamp": 1009000
            }
        ]

    @classmethod
    def set_user_preference(cls, key: str, value: str) -> None:
        pass

    @classmethod
    def set_gathering_rate(cls, component: str, metric: str, gathering_rate: int, argument: str = None) -> None:
        pass

    @classmethod
    def get_gathering_rate(cls, component: str, metric: str, argument: str = None) -> int:
        pass
