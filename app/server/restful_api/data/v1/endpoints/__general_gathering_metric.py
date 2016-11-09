from abc import abstractmethod, ABCMeta

from .__general_data_v1 import GeneralEndpointDataV1


class GeneralGatheringMetricEndpoint(GeneralEndpointDataV1, metaclass=ABCMeta):
    def _get(self) -> bool:
        component_type = self._get_component_type()
        component_arg = self._get_component_arg()
        component_metric = self._get_component_metric()

        gathering_rate_data = self._outbound_gate.get_gathering_rate(
            component_type,
            component_metric,
            component_arg
        )

        gathering_rate = 0
        if gathering_rate_data is not None:
            # TODO Change this in case the gathering_rate sturcture changes
            gathering_rate = gathering_rate_data[3]

        self._response_holder.set_body_data({
            "gathering_rate": gathering_rate
        })

        print(gathering_rate)

        return self.KEEP_PROCESSING()

    def _put(self) -> bool:
        request_body = self._request_holder.get_body()

        if "gathering_rate" not in request_body:
            return self.STOP_PROCESSING()  # TODO error - also check for number and number >= 500
        else:
            component_type = self._get_component_type()
            component_arg = self._get_component_arg()
            component_metric = self._get_component_metric()
            gathering_rate = request_body["gathering_rate"]

            self._outbound_gate.set_gathering_rate(
                component_type,
                component_metric,
                gathering_rate,
                component_arg
            )

            success_message = "SUCCESS - Set the gathering rate of components {0}-{1} metric {2} to {3}".format(
                component_type,
                component_arg,
                component_metric,
                gathering_rate
            )

            self._response_holder.set_body_data({
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