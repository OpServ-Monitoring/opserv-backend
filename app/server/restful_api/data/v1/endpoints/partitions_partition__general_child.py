from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class PartitionsPartitionGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @staticmethod
    def _get_parent():
        from .partitions_partition import PartitionsPartitionEndpoint

        return PartitionsPartitionEndpoint

    @staticmethod
    def _get_mandatory_parameters():
        from .partitions_partition import PartitionsPartitionEndpoint

        return [
            PartitionsPartitionEndpoint.get_partition_id_validator()
        ]

    @classmethod
    def _get_children(cls):
        return []

    def _get_component_type(self) -> str:
        return "partition"

    def _get_component_arg(self) -> str:
        return self._request_holder.get_params()["partition"]
