from misc.standalone_helper import decode_string, double_decode_string
from .__general_data_v1 import GeneralEndpointDataV1


class PartitionsPartitionEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        partition_id = self._request_holder.get_params()["partition"]
        partition_id = decode_string(partition_id)

        persisted_info = self._outbound_gate.get_last_measurement("partition", partition_id, "info")

        if persisted_info is not None:
            self._response_holder.update_body_data({
                "timestamp": persisted_info["timestamp"],
                "general-info": persisted_info["value"]
            })

        return True

    @classmethod
    def get_paths(cls):
        return [
            "/partitions/<string:partition>"
        ]

    @classmethod
    def get_name(cls):
        return "partition entity"

    @classmethod
    def _get_parent(cls):
        from .partitions import PartitionsEndpoint

        return PartitionsEndpoint

    @classmethod
    def _get_children(cls):
        from .partitions_partition_free import PartitionsPartitionFreeEndpoint
        from .partitions_partition_total import PartitionsPartitionTotalEndpoint
        from .partitions_partition_used import PartitionsPartitionUsedEndpoint

        return [
            ("/free", PartitionsPartitionFreeEndpoint),
            ("/total", PartitionsPartitionTotalEndpoint),
            ("/used", PartitionsPartitionUsedEndpoint)
        ]

    @classmethod
    def _get_mandatory_parameters(cls):
        return [
            cls.get_partition_id_validator()
        ]

    @classmethod
    def get_partition_id_validator(cls):
        return "partition", lambda x: cls._outbound_gate.is_argument_valid(
            "partition", double_decode_string(x))
