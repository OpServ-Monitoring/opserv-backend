from abc import abstractmethod, ABCMeta

from misc.standalone_helper import decode_string
from .__general_data_v1 import GeneralEndpointDataV1


class GeneralGatheringMetricEndpoint(GeneralEndpointDataV1, metaclass=ABCMeta):
    def _get(self) -> bool:
        component_arg = decode_string(self._get_component_arg())

        gathering_rate = self._outbound_gate.get_gathering_rate(
            self._get_component_type(),
            component_arg,
            self._get_component_metric()
        )

        if gathering_rate is None:
            gathering_rate = 0

        self._response_holder.update_body_data({
            "gathering_rate": gathering_rate
        })

        return self.KEEP_PROCESSING()

    def _put(self) -> bool:
        request_body = self._request_holder.get_body()

        if "gathering_rate" not in request_body or \
                not isinstance(request_body["gathering_rate"], int) or \
                (request_body["gathering_rate"] < 500 and request_body["gathering_rate"] != 0):
            # TODO Future version: Log and return error message

            return self.STOP_PROCESSING()
        else:
            component_type = self._get_component_type()
            component_arg = decode_string(self._get_component_arg())
            component_metric = self._get_component_metric()
            gathering_rate = request_body["gathering_rate"]

            self._outbound_gate.set_gathering_rate(
                component_type,
                component_arg,
                component_metric,
                gathering_rate
            )

            success_message = "SUCCESS - Set the gathering rate of components {0}-{1} metric {2} to {3}".format(
                component_type,
                component_arg,
                component_metric,
                gathering_rate
            )

            self._response_holder.update_body_data({
                "message": success_message
            })

            return self.KEEP_PROCESSING()

    @classmethod
    def _get_children(cls):
        return []

    @abstractmethod
    def _get_component_type(self) -> str:
        pass

    @abstractmethod
    def _get_component_arg(self) -> str:
        pass

    @abstractmethod
    def _get_component_metric(self) -> str:
        pass
