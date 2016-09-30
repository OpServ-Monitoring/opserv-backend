from .__general_data_v1 import GeneralEndpointDataV1


class GpusGpuEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        # TODO implement endpoint
        return True

    @staticmethod
    def get_paths():
        return [
            "/gpus/<string:gpu>"
        ]

    @staticmethod
    def get_name():
        return "gpu entity"

    @staticmethod
    def _get_parent():
        from .gpus import GpusEndpoint

        return GpusEndpoint

    @staticmethod
    def _get_children():
        return []

    @staticmethod
    def _get_mandatory_parameters():
        return [
            ("gpu", lambda x: int(x) > 4)
        ]