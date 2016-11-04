from .partitions_partition__general_child import PartitionsPartitionGeneralChildEndpoint


class PartitionsPartitionFreeEndpoint(PartitionsPartitionGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/partitions/<string:partition>/free"
        ]

    @staticmethod
    def get_name():
        return "partition free space measurement"

    def _get_component_metric(self) -> str:
        return "free"
