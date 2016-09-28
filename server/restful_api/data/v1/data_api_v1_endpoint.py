from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class DataApiV1Endpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        return True

    @staticmethod
    def get_paths():
        return [""]

    @staticmethod
    def get_name():
        # TODO useful name
        return "api version entry"

    @staticmethod
    def _get_parent():
        from server.restful_api.data.data_api_versions_endpoint import DataApiVersionsEndpoint

        return DataApiVersionsEndpoint

    @staticmethod
    def _get_children():
        from server.restful_api.data.v1.endpoints.cpus import CpusEndpoint
        from server.restful_api.data.v1.endpoints.cpucores import CpucoresEndpoint
        from server.restful_api.data.v1.endpoints.gpus import GpusEndpoint

        return [
            ("/cpus", CpusEndpoint),
            ("/cpu-cores", CpucoresEndpoint),
            ("/gpus", GpusEndpoint)
        ]
