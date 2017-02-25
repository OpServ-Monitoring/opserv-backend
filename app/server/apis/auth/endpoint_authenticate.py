import time

from server.apis.auth.token_generator import TokenGenerator
from server.apis.endpoint import Endpoint


class EndpointAuthenticate(Endpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "POST")

    def post(self):
        # TODO Authenticate
        # Get Username:Password from Auth-Header
        # Check password and load user_id from database

        self.respond({
            "access_token": self.generate_jwt_token("0")
        })

    @classmethod
    def generate_jwt_token(cls, uid) -> str:
        now = int(time.time())
        valid_seconds = 60 * 60 * 6  # 6 hours validity

        payload = {
            "uid": uid,
            "iat": now,
            "exp": now + valid_seconds
        }

        return TokenGenerator.encode_token(payload).decode("utf-8")
