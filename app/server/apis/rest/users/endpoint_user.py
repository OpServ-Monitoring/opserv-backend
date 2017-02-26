from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointUser(AuthenticatedEndpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "GET")
        self.add_header("Allow", "DELETE")
        self.add_header("Allow", "PATCH")

    def get(self, user_id):
        print("get")

    def delete(self, user_id):
        print("delete")

    def patch(self, user_id):
        print("patch")
