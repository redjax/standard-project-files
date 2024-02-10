from __future__ import annotations

from typing import Union

from dynaconf import Dynaconf
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

DYNACONF_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)

## Uncomment to load database settings from environment
# DYNACONF_DB_SETTINGS: Dynaconf = Dynaconf(
#     environments=True,
#     envvar_prefix="DB",
#     settings_files=["settings.toml", ".secrets.toml"],
# )


class AppSettings(BaseSettings):
    env: str = Field(default=DYNACONF_SETTINGS.ENV, env="ENV")
    container_env: bool = Field(
        default=DYNACONF_SETTINGS.CONTAINER_ENV, env="CONTAINER_ENV"
    )
    log_level: str = Field(default=DYNACONF_SETTINGS.LOG_LEVEL, env="LOG_LEVEL")


## Uncomment if you're configuring a database for the app
# class DBSettings(BaseSettings):
#     drivername: str = Field(
#         default=DYNACONF_DB_SETTINGS.DB_DRIVERNAME, env="DB_DRIVERNAME"
#     )
#     user: str | None = Field(
#         default=DYNACONF_DB_SETTINGS.DB_USERNAME, env="DB_USERNAME"
#     )
#     password: str | None = Field(
#         default=DYNACONF_DB_SETTINGS.DB_PASSWORD, env="DB_PASSWORD", repr=False
#     )
#     host: str | None = Field(default=DYNACONF_DB_SETTINGS.DB_HOST, env="DB_HOST")
#     port: Union[str, int, None] = Field(
#         default=DYNACONF_DB_SETTINGS.DB_PORT, env="DB_PORT"
#     )
#     database: str = Field(default=DYNACONF_DB_SETTINGS.DB_DATABASE, env="DB_DATABASE")

#     @field_validator("port")
#     def validate_db_port(cls, v) -> int:
#         if v is None or v == "":
#             return None
#         elif isinstance(v, int):
#             return v
#         elif isinstance(v, str):
#             return int(v)
#         else:
#             raise ValidationError


settings: AppSettings = AppSettings()
## Uncomment if you're configuring a database for the app
# db_settings: DBSettings = DBSettings()
