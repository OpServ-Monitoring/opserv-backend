from abc import ABCMeta

from server.restful_api.data.v1.endpoints.__general_gathering_metric import GeneralGatheringMetricEndpoint


class SystemGeneralChildEndpoint(GeneralGatheringMetricEndpoint, metaclass=ABCMeta):
    def _get_component_type(self) -> str:
        return "system"

    def _get_component_arg(self) -> str:
        return None

    @classmethod
    def _get_parent(cls):
        from .system import SystemEndpoint

        return SystemEndpoint
