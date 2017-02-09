from .partitions_partition__general_child import PartitionsPartitionGeneralChildEndpoint


class PartitionsPartitionUsedEndpoint(PartitionsPartitionGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/partitions/<string:partition>/used"
        ]

    @classmethod
    def get_name(cls):
        return "partition used space measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "used"
