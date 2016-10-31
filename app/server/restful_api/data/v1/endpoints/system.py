from ....general.endpoint import Endpoint


# TODO Implement endpoint
class SystemEndpoint(Endpoint):
    def _post_process(self) -> bool:
        return Endpoint.KEEP_PROCESSING()

    def _put(self) -> bool:
        pass

    def _post(self) -> bool:
        pass

    @staticmethod
    def get_paths():
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

    @staticmethod
    def _get_parent():
        from ..data_api_v1_endpoint import DataApiV1Endpoint

        return DataApiV1Endpoint

    def _delete(self) -> bool:
        pass

    def _get(self) -> bool:
        pass

    @staticmethod
    def get_name():
        return "system components"
