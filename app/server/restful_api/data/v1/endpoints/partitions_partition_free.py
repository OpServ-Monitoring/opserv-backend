from .partitions_partition__general_child import PartitionsPartitionGeneralChildEndpoint


class PartitionsPartitionFreeEndpoint(PartitionsPartitionGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/partitions/<string:partition>/free"
        ]

    @classmethod
    def get_name(cls):
        return "partition free space measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "free"
