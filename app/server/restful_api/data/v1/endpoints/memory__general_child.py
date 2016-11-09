from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class MemoryGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    def _get_component_type(self) -> str:
        return "memory"

    def _get_component_arg(self) -> str:
        return None

    @classmethod
    def _get_parent(cls):
        from .memory import MemoryEndpoint

        return MemoryEndpoint
