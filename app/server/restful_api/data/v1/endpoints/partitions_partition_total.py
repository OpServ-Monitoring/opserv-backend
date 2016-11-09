from .partitions_partition__general_child import PartitionsPartitionGeneralChildEndpoint


class PartitionsPartitionTotalEndpoint(PartitionsPartitionGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/partitions/<string:partition>/total"
        ]

    @classmethod
    def get_name(cls):
        return "partition total space measurement"

    def _get_component_metric(self) -> str:
        return "total"
