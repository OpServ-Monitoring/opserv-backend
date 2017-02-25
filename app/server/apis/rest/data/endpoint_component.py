import misc.constants
from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointComponent(AuthenticatedEndpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "GET")

    def get(self, system_metric, component_arg):
        if system_metric not in misc.constants.SYSTEM_METRICS_TO_COMPS:
            self.send_error(400)  # TODO Add details
            return

        component_type = misc.constants.SYSTEM_METRICS_TO_COMPS[system_metric]
        valid_args = self._outbound_gate.get_valid_arguments(component_type)

        if component_arg not in valid_args:
            self.send_error(400)  # TODO Add details
            return

        data = []
        path = self.get_path()

        metrics = misc.constants.implemented_hardware[component_type]
        for metric in metrics:
            data.append(
                self.get_resource_reference(
                    component_type + "-" + component_arg + "-metric",
                    metric,
                    path
                )
            )

        self.respond(data)
