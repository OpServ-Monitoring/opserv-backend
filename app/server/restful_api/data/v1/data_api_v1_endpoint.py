from app.server.restful_api.data.v1.endpoints.root__general_child import RootGeneralChildEndpoint


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
        from app.server.restful_api.data.v1.endpoints.cpus import CpusEndpoint
        from app.server.restful_api.data.v1.endpoints.cpucores import CpucoresEndpoint
        from app.server.restful_api.data.v1.endpoints.gpus import GpusEndpoint

        return [
            ("/cpus", CpusEndpoint),
            ("/cpu-cores", CpucoresEndpoint),
            ("/gpus", GpusEndpoint)
        ]
