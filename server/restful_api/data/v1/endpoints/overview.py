from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class OverviewEndpoint(GeneralEndpointDataV1):

    def _get(self):
        # TODO Implement endpoint
        pass

    @staticmethod
    def get_paths():
        return [""]
