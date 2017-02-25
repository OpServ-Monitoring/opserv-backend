from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointUsers(AuthenticatedEndpoint):
    def get(self):
        print("get")
        # If not manage_users
        #   Show only self
        # else
        #   Show all users
        pass

    def post(self):
        print("post")
        # If not manage_users
        #   403
        # else
        #   Add user
        pass
