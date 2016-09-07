from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class ComponentsEndpoint(GeneralEndpointDataV1):
    def _get(self):
        self._response.set_body({
            "message": "Not yet implemented."
        })

    @staticmethod
    def get_paths():
        return [
            "/components"
        ]
