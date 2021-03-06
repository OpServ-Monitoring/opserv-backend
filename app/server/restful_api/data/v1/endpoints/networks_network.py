from misc.standalone_helper import decode_string, double_decode_string
from .__general_data_v1 import GeneralEndpointDataV1


class NetworksNetworkEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        network_id = self._request_holder.get_params()["network"]
        network_id = decode_string(network_id)
        persisted_info = self._outbound_gate.get_last_measurement("network", network_id, "info")

        if persisted_info is not None:
            self._response_holder.update_body_data({
                "timestamp": persisted_info["timestamp"],
                "general-info": persisted_info["value"]
            })

        return True

    @classmethod
    def get_paths(cls):
        return [
            "/networks/<string:network>"
        ]

    @classmethod
    def get_name(cls):
        return "network entity"

    @classmethod
    def _get_parent(cls):
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

    @classmethod
    def _get_mandatory_parameters(cls):
        return [
            cls.get_network_id_validator()
        ]

    @classmethod
    def get_network_id_validator(cls):
        return "network", lambda x: cls._outbound_gate.is_argument_valid(
            "network", double_decode_string(x))
