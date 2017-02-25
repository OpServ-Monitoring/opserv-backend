import jwt


class TokenGenerator:
    __secret = "secret"  # TODO Generate random secret os.urandom(32)

    @classmethod
    def encode_token(cls, payload):
        return jwt.encode(
            payload,
            cls.__secret,
            algorithm='HS256'
        )

    @classmethod
    def decode_token(cls, encoded_jwt_token):
        return jwt.decode(
            encoded_jwt_token,
            cls.__secret,
            algorithms=['HS256']
        )
