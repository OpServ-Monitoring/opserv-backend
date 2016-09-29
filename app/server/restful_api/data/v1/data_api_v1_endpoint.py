from .endpoints.root__general_child import RootGeneralChildEndpoint


class DataApiV1Endpoint(RootGeneralChildEndpoint):
    def _get(self) -> bool:
        # no data section available
        return self.KEEP_PROCESSING()

    @staticmethod
    def get_paths():
        return [""]

    @staticmethod
    def get_name():
        return "data API v1 entry"

    @staticmethod
    def _get_children():
        from .endpoints.cpus import CpusEndpoint
        from .endpoints.cpucores import CpucoresEndpoint
        from .endpoints.gpus import GpusEndpoint

        return [
            ("/cpus", CpusEndpoint),
            ("/cpu-cores", CpucoresEndpoint),
            ("/gpus", GpusEndpoint)
        ]
