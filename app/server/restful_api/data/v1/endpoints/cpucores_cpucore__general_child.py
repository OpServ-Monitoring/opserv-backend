from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpucoresCpucoreGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @classmethod
    def _get_parent(cls):
        from .cpucores_cpucore import CpucoresCpucoreEndpoint

        return CpucoresCpucoreEndpoint

    @classmethod
    def _get_mandatory_parameters(cls):
        from .cpucores_cpucore import CpucoresCpucoreEndpoint

        return [
            CpucoresCpucoreEndpoint.get_cpucore_id_validator()
        ]

    @classmethod
    def _get_children(cls):
        return []

    def _get_component_arg(self) -> str:
        return self._request_holder.get_params()["cpu_core"]

    def _get_component_type(self) -> str:
        return "core"
