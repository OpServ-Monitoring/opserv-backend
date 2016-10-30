from .__general_data_v1 import GeneralEndpointDataV1


class NetworksNetworkEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        # TODO implement endpoint
        from app.database.unified_database_interface import UnifiedDatabaseInterface
        network_id = self._request_holder.get_params()["network"]

        persisted_info = UnifiedDatabaseInterface.get_measurement_data_reader().get_last_value("network", network_id,
                                                                                               "info")

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info[0],
                "general-info": persisted_info[1]
            })

        return True

    @staticmethod
    def get_paths():
        return [
            "/networks/<string:network>"
        ]

    @staticmethod
    def get_name():
        return "network entity"

    @staticmethod
    def _get_parent():
        from .networks import NetworksEndpoint

        return NetworksEndpoint

    @classmethod
    def _get_children(cls):
        return [
        ]

    @staticmethod
    def _get_mandatory_parameters():
        return [
            NetworksNetworkEndpoint.get_gpu_id_validator()
        ]

    @staticmethod
    def get_gpu_id_validator():
        # TODO Validate network id
        return "network", lambda x: True
