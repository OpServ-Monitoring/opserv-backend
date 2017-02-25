from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointPreferences(AuthenticatedEndpoint):
    def get(self):
        print("get")
        pass

    def post(self):
        print("post")
        pass
