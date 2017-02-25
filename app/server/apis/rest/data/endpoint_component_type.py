import misc.constants
from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointComponentType(AuthenticatedEndpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "GET")

    def get(self, system_metric):
        if system_metric not in misc.constants.SYSTEM_METRICS_TO_COMPS:
            self.send_error(400)  # TODO Add details
            return

        component_type = misc.constants.SYSTEM_METRICS_TO_COMPS[system_metric]
        valid_args = self._outbound_gate.get_valid_arguments(component_type)
        path = self.get_path()

        data = []

        for arg in valid_args:
            data.append(
                self.get_resource_reference(
                    component_type + "-component",
                    arg,
                    path
                )
            )

        self.respond(data)
