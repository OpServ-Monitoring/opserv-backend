from abc import ABCMeta, abstractmethod

from database.unified_database_interface import UnifiedDatabaseInterface
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
        realtime_data = cls.__get_current_children_ids()
        persisted_data = cls.__get_persisted_children_ids()

        return cls.__merge_two_lists(realtime_data, persisted_data)

    @classmethod
    def __get_current_children_ids(cls) -> list:
        # TODO improve method

        hardware_value_type = cls._get_hardware_value_type()

        from misc import data_manager
        data = data_manager.getMeasurement(component="system", metric=hardware_value_type)

        if data is not None and 'value' in data:
            return data['value']
        return []

    @classmethod
    def __get_persisted_children_ids(cls) -> list:
        component_type = cls._get_component_type()

        return UnifiedDatabaseInterface.get_component_args(component_type)

    @classmethod
    def __merge_two_lists(cls, first_list, second_list):
        return first_list + list(set(second_list) - set(first_list))

        # TODO Is this the right place for this? -> Extract to some data providing interface
