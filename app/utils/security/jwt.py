from datetime import datetime, timedelta, UTC

import jwt

from app.core.config import AuthConfig
from app.domain.common import exceptions


class JWT:
    def __init__(self, auth: AuthConfig):
        self.auth = auth

    def create_access_token(self, data: dict) -> str:
        return self._create_token(
            token_type='access_token',
            lifetime=timedelta(minutes=self.auth.access_token_expire_minutes),
            key=self.auth.secret_key.get_secret_value(),
            data={'user': data},
        )

    def create_refresh_token(self, data: dict) -> str:
        return self._create_token(
            token_type='refresh_token',
            lifetime=timedelta(minutes=self.auth.refresh_token_expire_minutes),
            key=self.auth.refresh_key.get_secret_value(),
            data={'user': data},
        )

    def decode_access_token(self, token):
        return self.__decode(token, self.auth.secret_key.get_secret_value())

    def decode_refresh_token(self, token):
        return self.__decode(token, self.auth.refresh_key.get_secret_value())

    def _create_token(self, token_type: str, lifetime: timedelta, key: str, data: dict) -> str:
        payload = data.copy()
        payload.update(
            {
                'exp': datetime.now(UTC) + lifetime,
                'iat': datetime.now(UTC),
                'sub': token_type,
            }
        )

        return self.__encode(payload, key)

    def __decode(self, token: str, key: str) -> dict | None:
        try:
            payload = jwt.decode(token, key, algorithms=[self.auth.algorithm])
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.TokenExpired
        except jwt.exceptions.PyJWTError:
            raise exceptions.TokenInvalid
        return payload

    def __encode(self, payload: dict, key: str) -> str:
        return jwt.encode(payload, key, algorithm=self.auth.algorithm)
