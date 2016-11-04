from abc import ABCMeta, abstractmethod

from server.data_gates.default_data_gate import DefaultDataGate
from .__general_data_v1 import GeneralEndpointDataV1
from ....general.endpoint import Endpoint


class RootGeneralChildEndpoint(GeneralEndpointDataV1, metaclass=ABCMeta):
    @staticmethod
    def _get_parent():
        from ...data_api_versions_endpoint import DataApiVersionsEndpoint

        return DataApiVersionsEndpoint

    def _get(self) -> bool:
        # no data section available
        return self.KEEP_PROCESSING()

    @classmethod
    def _get_children(cls):
        endpoint_type = cls._get_children_endpoint_type()

        children = []

        ids = cls.__get_children_ids()
        for child_id in ids:
            children.append(("/" + str(child_id), endpoint_type))

        return children

    @staticmethod
    @abstractmethod
    def _get_hardware_value_type() -> str:
        pass

    @staticmethod
    @abstractmethod
    def _get_component_type() -> str:
        pass

    @staticmethod
    @abstractmethod
    def _get_children_endpoint_type() -> Endpoint:
        pass

    @classmethod
    def __get_children_ids(cls) -> list:
        return DefaultDataGate.get_valid_arguments(cls._get_hardware_value_type())