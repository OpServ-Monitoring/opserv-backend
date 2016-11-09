from collections import Iterable

from ....general.endpoint import Endpoint


# TODO Implement endpoint
class SystemEndpoint(Endpoint):
    def _post_process(self) -> bool:
        return Endpoint.KEEP_PROCESSING()

    def _put(self) -> bool:
        pass

    def _post(self) -> bool:
        pass

    @classmethod
    def get_paths(cls):
        return [
            "/system"
        ]

    @classmethod
    def _get_children(cls) -> Iterable:
        from .system_cpucores import SystemCpucoresEndpoint
        from .system_cpus import SystemCpusEndpoint
        from .system_disks import SystemDisksEndpoint
        from .system_gpus import SystemGpusEndpoint
        from .system_networks import SystemNetworksEndpoint
        from .system_partitions import SystemPartitionsEndpoint
        from .system_processes import SystemProcessesEndpoint

        return [
            ("/cpucores", SystemCpucoresEndpoint),
            ("/cpus", SystemCpusEndpoint),
            ("/disks", SystemDisksEndpoint),
            ("/gpus", SystemGpusEndpoint),
            ("/networks", SystemNetworksEndpoint),
            ("/partitions", SystemPartitionsEndpoint),
            ("/processes", SystemProcessesEndpoint)
        ]

    @classmethod
    def _get_parent(cls):
        from ..data_api_v1_endpoint import DataApiV1Endpoint

        return DataApiV1Endpoint

    def _delete(self) -> bool:
        pass

    def _get(self) -> bool:
        pass

    @classmethod
    def get_name(cls):
        return "system components"
