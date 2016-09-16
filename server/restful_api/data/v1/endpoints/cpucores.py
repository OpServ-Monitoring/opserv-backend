from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpucoresEndpoint(GeneralEndpointDataV1):
    def _get(self):
        # TODO general info
        pass

    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/cpu-cores",
            "/cpu-cores"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.data_api_v1_endpoint import DataApiV1Endpoint

        return DataApiV1Endpoint.get_name()

    def _get_children(self):
        # TODO Implement dynamic children
        return []
