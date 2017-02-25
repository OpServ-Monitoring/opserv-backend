from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointUser(AuthenticatedEndpoint):
    def get(self, user_id):
        print("get")

    def delete(self, user_id):
        print("delete")

    def patch(self, user_id):
        print("patch")
