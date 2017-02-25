import misc.constants
from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointApiRoot(AuthenticatedEndpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "GET")

    def get(self):
        data = []
        path = self.get_path()

        for system_metric in misc.constants.system_metrics:
            data.append(
                self.get_resource_reference(
                    "component_type",
                    system_metric,
                    path
                )
            )

        self.respond(data)
