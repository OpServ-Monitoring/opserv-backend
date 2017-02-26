import base64
import time

from server.apis.auth.token_generator import TokenGenerator
from server.apis.endpoint import Endpoint


class EndpointAuthenticate(Endpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "POST")

    def post(self):
        authorization_header = self.request.headers.get("Authorization")

        if authorization_header is None or not authorization_header.startswith('Basic '):
            self.send_error(400)  # todo details
            return

        decoded_user_name_and_password = base64.b64decode(authorization_header[6:]).decode("utf-8")
        user_name, user_password = decoded_user_name_and_password.split(':', 2)

        # TOOD Exchange with call to data gate
        from database.unified_database_interface import UnifiedDatabaseInterface
        users_writer_reader = UnifiedDatabaseInterface.get_users_writer_reader()

        if users_writer_reader.is_password_valid(user_name, user_password):
            user = users_writer_reader.get_user(user_name)
            user_id = user[0]

            self.respond({
                "access_token": self.generate_jwt_token(str(user_id))
            })
        else:
            self.send_error(403)  # todo details invalid password or username

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
