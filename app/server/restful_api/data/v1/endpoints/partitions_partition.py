from .__general_data_v1 import GeneralEndpointDataV1


class PartitionsPartitionEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        partition_id = self._request_holder.get_params()["partition"]

        persisted_info = self._outbound_gate.get_last_measurement("partition", "info", partition_id)

        if persisted_info is not None:
            self._response_holder.set_body_data({
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
        from server.data_gates.default_data_gate import DefaultDataGate
        return "partition", lambda x: cls._outbound_gate.is_argument_valid(
            DefaultDataGate.decode_argument(DefaultDataGate.decode_argument(x)), "partition")
