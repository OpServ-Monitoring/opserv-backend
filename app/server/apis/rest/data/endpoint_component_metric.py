import misc.constants
from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointComponentMetric(AuthenticatedEndpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "GET")

    def get(self, system_metric, component_arg, metric):
        if system_metric not in misc.constants.SYSTEM_METRICS_TO_COMPS:
            self.send_error(400)  # TODO Add details
            return

        component_type = misc.constants.SYSTEM_METRICS_TO_COMPS[system_metric]
        valid_args = self._outbound_gate.get_valid_arguments(component_type)

        if component_arg not in valid_args:
            self.send_error(400)  # TODO Add details
            return

        metrics = misc.constants.implemented_hardware[component_type]
        if metric not in metrics:
            self.send_error(400)  # TODO Add details
            return

        data = {
            "type": component_type + "-" + component_arg + "-metric",
            "id": metric,
            "attributes": {
                "gathering-rate": 1000,
                "persistence": True,
                "values": [{
                    "timestamp": 0,
                    "min": 34,
                    "avg": 34,
                    "max": 34,
                    "count": 1
                }]
            }
        }

        self.respond(data)
