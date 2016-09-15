from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpucoresEndpoint(GeneralEndpointDataV1):
    def _get(self):
        # TODO general info
        pass

    @staticmethod
    def get_paths():
        return [
            "/components/cpus/<string:cpu>/cpu-cores",
            "/components/cpu-cores"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.endpoints.components import ComponentsEndpoint

        return ComponentsEndpoint.get_name()

    def _get_children(self):
        # TODO Implement dynamic children
        return []
