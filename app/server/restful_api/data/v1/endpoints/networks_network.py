from .__general_data_v1 import GeneralEndpointDataV1


class NetworksNetworkEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        network_id = self._request_holder.get_params()["network"]

        persisted_info = self._outbound_gate.get_last_measurement("network", "info", network_id)

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info["timestamp"],
                "general-info": persisted_info["value"]
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
        from .networks_network_receivepersec import NetworksNetworkReceivepersecEndpoint
        from .networks_network_transmitpersec import NetworksNetworkTransmitpersecEndpoint

        return [
            ("/receivepersec", NetworksNetworkReceivepersecEndpoint),
            ("/transmitpersec", NetworksNetworkTransmitpersecEndpoint)
        ]

    @staticmethod
    def _get_mandatory_parameters():
        return [
            NetworksNetworkEndpoint.get_network_id_validator()
        ]

    @classmethod
    def get_network_id_validator(cls):
        return "network", lambda x: cls._outbound_gate.is_argument_valid(x, "networks")
