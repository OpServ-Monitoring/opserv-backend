from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class SystemEndpoint(GeneralEndpointDataV1):
    @classmethod
    def get_paths(cls):
        return [
            "/system"
        ]

    @classmethod
    def _get_children(cls) -> list:
        from .system_cpucores import SystemCpucoresEndpoint
        from .system_cpus import SystemCpusEndpoint
        from .system_disks import SystemDisksEndpoint
        from .system_gpus import SystemGpusEndpoint
        from .system_networks import SystemNetworksEndpoint
        from .system_partitions import SystemPartitionsEndpoint
        from .system_processes import SystemProcessesEndpoint

        return [
            ("/cpu-cores", SystemCpucoresEndpoint),
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

    def _get(self) -> bool:
        # No data section available

        return self.KEEP_PROCESSING()

    @classmethod
    def get_name(cls):
        return "system components"
