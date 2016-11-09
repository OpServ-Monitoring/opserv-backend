from .root__general_child import RootGeneralChildEndpoint
from ....general.endpoint import Endpoint


class PartitionsEndpoint(RootGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/partitions"
        ]

    @classmethod
    def get_name(cls):
        return "partition entities"

    @classmethod
    def _get_hardware_value_type(cls) -> str:
        return "partitions"

    @classmethod
    def _get_children_endpoint_type(cls) -> Endpoint:
        from .partitions_partition import PartitionsPartitionEndpoint

        return PartitionsPartitionEndpoint
