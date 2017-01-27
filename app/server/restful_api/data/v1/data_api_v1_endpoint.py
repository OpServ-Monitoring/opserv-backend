from .endpoints.__general_data_v1 import GeneralEndpointDataV1
from ..data_api_versions_endpoint import DataApiVersionsEndpoint


class DataApiV1Endpoint(GeneralEndpointDataV1):
    @classmethod
    def _get_parent(cls):
        return DataApiVersionsEndpoint

    def _get(self) -> bool:
        # no data section available
        return self.KEEP_PROCESSING()

    @classmethod
    def get_paths(cls):
        return [""]

    @classmethod
    def get_name(cls):
        return "data API v1 entry"

    @classmethod
    def _get_children(cls):
        from .endpoints.cpus import CpusEndpoint
        from .endpoints.cpucores import CpucoresEndpoint
        from .endpoints.disks import DisksEndpoint
        from .endpoints.gpus import GpusEndpoint
        from .endpoints.memory import MemoryEndpoint
        from .endpoints.networks import NetworksEndpoint
        from .endpoints.partitions import PartitionsEndpoint
        from .endpoints.processes import ProcessesEndpoint
        from .endpoints.system import SystemEndpoint
        from .endpoints.gatheringrates import GatheringRatesEndpoint

        return [
            ("/cpus", CpusEndpoint),
            ("/cpu-cores", CpucoresEndpoint),
            ("/gpus", GpusEndpoint),
            ("/disks", DisksEndpoint),
            ("/memory", MemoryEndpoint),
            ("/networks", NetworksEndpoint),
            ("/partitions", PartitionsEndpoint),
            ("/processes", ProcessesEndpoint),
            ("/system", SystemEndpoint),
            ("/gathering-rates", GatheringRatesEndpoint)
        ]
