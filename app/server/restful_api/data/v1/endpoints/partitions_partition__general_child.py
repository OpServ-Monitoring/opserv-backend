from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class PartitionsPartitionGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @classmethod
    def _get_parent(cls):
        from .partitions_partition import PartitionsPartitionEndpoint

        return PartitionsPartitionEndpoint

    @classmethod
    def _get_mandatory_parameters(cls):
        from .partitions_partition import PartitionsPartitionEndpoint

        return [
            PartitionsPartitionEndpoint.get_partition_id_validator()
        ]

    @classmethod
    def _get_children(cls):
        return []

    @classmethod
    def _get_component_type(cls) -> str:
        return "partition"

    def _get_component_arg(self) -> str:
        return self._request_holder.get_params()["partition"]
