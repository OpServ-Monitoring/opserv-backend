from .partitions_partition__general_child import PartitionsPartitionGeneralChildEndpoint


class PartitionsPartitionTotalEndpoint(PartitionsPartitionGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/partitions/<string:partition>/total"
        ]

    @staticmethod
    def get_name():
        return "partition total space measurement"

    def _get_component_metric(self) -> str:
        return "total"
