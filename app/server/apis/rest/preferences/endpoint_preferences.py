from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointPreferences(AuthenticatedEndpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "GET")

    def get(self):
        path = self.get_path()

        data = []
        for preference_key in self._outbound_gate.get_user_preference_keys():
            data.append(
                self.get_resource_reference(
                    "preference",
                    preference_key,
                    path
                )
            )

        self.respond(data)
