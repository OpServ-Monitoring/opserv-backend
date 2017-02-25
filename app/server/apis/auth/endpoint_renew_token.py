from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointRenewToken(AuthenticatedEndpoint):
    def post(self):
        from server.apis.auth.endpoint_authenticate import EndpointAuthenticate

        self.respond({
            "access_token": EndpointAuthenticate.generate_jwt_token(self.current_user)
        })
