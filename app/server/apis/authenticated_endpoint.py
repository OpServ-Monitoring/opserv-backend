import logging

import jwt

from .auth.token_generator import TokenGenerator
from .endpoint import Endpoint

log = logging.getLogger("opserv." + __name__)


class AuthenticatedEndpoint(Endpoint):
    def get_current_user(self):
        """
        Overrides the built-in function to get the user id based on a JWT-token.
        If there is no token included in the Authorization header None is returned.
        In case the token is not valid an corresponding exception is raised.

        :return: The user id as a string or None if the uid couldn't be extracted
        :raises jwt.InvalidIssuedAtError: Raised if the IAT-claim is less than the last time the user password changed
        :raises jwt.ExpiredSignatureError: Raised if the EXT-claim is less than the current UNIX time
        :raises jwt.InvalidTokenError: Raised if the token is invalid for reasons other than the above mentioned
        """
        auth_header = self.request.headers.get('Authorization')

        if auth_header is not None and auth_header.startswith("Bearer "):
            encoded_jwt_token = auth_header[7:]

            payload = TokenGenerator.decode_token(encoded_jwt_token)

            # TODO Should we check if payload["iat"] < last password change?
            if False:
                raise jwt.InvalidIssuedAtError

            return payload["uid"]
        return None

    def prepare(self):
        """
        Ensures that the caller is a validated user
        """
        super().prepare()

        try:
            if self.current_user is None:
                self.send_error(401)  # TODO Add details

        except jwt.InvalidIssuedAtError:
            log.error("The IAT-claim of the passed token is less than the last time the user password changed")
            self.send_error(401, summary="invalidated token")

        except jwt.ExpiredSignatureError:
            log.error("The EXT-claim of the passed token is less than the current UNIX time")
            self.send_error(401, summary="expired token")

        except jwt.InvalidTokenError:
            log.error("The passed token could not be validated")
            self.send_error(401, summary="invalid token")
