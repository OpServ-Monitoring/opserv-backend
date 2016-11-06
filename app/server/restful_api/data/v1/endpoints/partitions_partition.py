from .__general_data_v1 import GeneralEndpointDataV1


class PartitionsPartitionEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        partition_id = self._request_holder.get_params()["partition"]

        persisted_info = self._outbound_gate.get_last_measurement("partition", partition_id, "info")

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info[0],
                "general-info": persisted_info[1]
            })

        return True

    @staticmethod
    def get_paths():
        return [
            "/partitions/<string:partition>"
        ]

    @staticmethod
    def get_name():
        return "partition entity"

    @staticmethod
    def _get_parent():
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

    @staticmethod
    def _get_mandatory_parameters():
        return [
            PartitionsPartitionEndpoint.get_partition_id_validator()
        ]

    @classmethod
    def get_partition_id_validator(cls):
        return "partition", lambda x: cls._outbound_gate.is_argument_valid(x, "partitions")
