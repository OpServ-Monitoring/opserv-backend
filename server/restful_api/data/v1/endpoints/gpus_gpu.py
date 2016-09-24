from server.restful_api.data.v1.endpoints.__general_parameterized import GeneralEndpointParameterized


class GpusGpuEndpoint(GeneralEndpointParameterized):
    def _get(self):
        # TODO general info
        pass

    @staticmethod
    def get_paths():
        return [
            "/gpus/<string:gpu>"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent():
        from server.restful_api.data.v1.endpoints.gpus import GpusEndpoint

        return GpusEndpoint

    def _get_children(self):
        return []

    @staticmethod
    def _get_mandatory_parameters():
        return [
            GeneralEndpointParameterized._build_parameter("gpu", lambda x: int(x) > 4)
        ]
