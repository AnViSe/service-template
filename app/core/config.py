from functools import partial
from pathlib import Path

from pydantic import BaseModel, Field, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

env_model_config = partial(
    SettingsConfigDict,
    env_file='.env',
    env_file_encoding='utf-8',
    extra='ignore',
)


class LoggingConfig(BaseSettings):
    model_config = env_model_config(env_prefix='LOG_')

    level: str = Field(default='DEBUG', init=False)
    logger_name: str = Field(default='srv.template', init=False)

    file_path: Path = Field(default='logs', init=False)
    file_name: str = Field(default='service.log', init=False)
    file_size: int = Field(default=5, init=False)
    file_count: int = Field(default=10, init=False)

    json_format: bool = Field(default=True, init=False)

    echo_sql: bool = Field(default=True, init=False)


class AppConfig(BaseSettings):
    model_config = env_model_config(env_prefix='APP_')

    debug: bool = Field(default=True, init=False)
    version: str = Field(default='0.0.1', init=False)
    title: str = Field(default='Application Title', init=False)
    description: str | None = Field(default=None, init=False)
    api_url: str = Field(default='/api/v1/template', init=False)
    bus_group: str = Field(default='srv-template', init=False)

    app_id: int | None = Field(default=None, init=False)

    @property
    def openapi_url(self) -> str:
        return f'{self.api_url}/openapi.json'

    def consumer_name(self) -> str:
        return f'{self.bus_group}-{self.app_id}'


class AuthConfig(BaseSettings):
    model_config = env_model_config(env_prefix='AUTH_')

    api_url: str = Field(default='/api/v1/template', init=False)
    algorithm: str = Field(default='HS256', init=False)
    secret_key: SecretStr = Field(default='secret', init=False)
    refresh_key: SecretStr = Field(default='refresh', init=False)
    access_token_expire_minutes: int = Field(default=600, init=False)
    refresh_token_expire_minutes: int = Field(default=38400, init=False)


class PostgresConfig(BaseSettings):
    model_config = env_model_config(env_prefix='DB_MAIN_')

    host: str = Field(default='localhost', init=False)
    port: int = Field(default=5432, init=False)
    name: str = Field(default='srv-template', init=False)
    user: str | None = Field(default=None, init=False)
    password: SecretStr | None = Field(default=None, init=False)

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=self.user,
            password=self.password.get_secret_value() if self.password else None,
            host=self.host,
            port=self.port,
            path=self.name,
        )

    def url(self, async_fallback: bool = False) -> str:
        url = f'postgresql+asyncpg://{self.user}'
        if self.password:
            url += f':{self.password.get_secret_value()}'
        url += f'@{self.host}:{self.port}/{self.name}'
        if async_fallback:
            url += '?async_fallback=True'
        return url


class RedisConfig(BaseSettings):

    host: str = Field(default='localhost', init=False)
    port: int = Field(default=6379, init=False)
    name: str | int = Field(default=0, init=False)
    ssl: bool = Field(default=False, init=False)
    user: str | None = Field(default=None, init=False)
    password: SecretStr | None = Field(default=None, init=False)

    @property
    def dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme='rediss' if self.ssl else 'redis',
            username=self.user,
            password=self.password.get_secret_value() if self.password else None,
            host=self.host,
            port=self.port,
            path=f'{self.name}'
        )


class BusConfig(RedisConfig):
    model_config = env_model_config(env_prefix='DB_BUS_')

    name: str | int = Field(default=10, init=False)


class CacheConfig(RedisConfig):
    model_config = env_model_config(env_prefix='DB_CACHE_')

    name: str | int = Field(default=11, init=False)


class Config(BaseModel):
    app: AppConfig = Field(default_factory=lambda: AppConfig())
    auth: AuthConfig = Field(default_factory=lambda: AuthConfig())
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig())
    bus: BusConfig = Field(default_factory=lambda: BusConfig())
    cache: CacheConfig = Field(default_factory=lambda: CacheConfig())
    logging: LoggingConfig = Field(default_factory=lambda: LoggingConfig())


config = Config()
