import jwt

from app.domain.common import exceptions


class JWT:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key: str = secret_key
        self.algorithm: str = algorithm

    def decode(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.TokenExpired
        except jwt.exceptions.PyJWTError:
            raise exceptions.TokenInvalid
        return payload

    def encode(self, payload: dict, expire_at: int | float | None = None) -> str:
        if expire_at:
            payload['exp'] = expire_at
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
