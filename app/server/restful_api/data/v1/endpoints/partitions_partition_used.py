from .partitions_partition__general_child import PartitionsPartitionGeneralChildEndpoint


class PartitionsPartitionUsedEndpoint(PartitionsPartitionGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/partitions/<string:partition>/used"
        ]

    @staticmethod
    def get_name():
        return "partition used space measurement"

    def _get_component_metric(self) -> str:
        return "used"
