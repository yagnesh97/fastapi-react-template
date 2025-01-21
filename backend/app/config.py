import pathlib

import tomllib
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utilities.enums import Environments

path = pathlib.Path(__file__).parent.absolute()
with open(f"{path}/../pyproject.toml", mode="rb") as f:
    project_data = tomllib.load(f)

app_version = project_data["tool"]["poetry"]["version"]
app_name = project_data["tool"]["poetry"]["name"]
app_title = project_data["tool"]["metadata"]["title"]
app_description = project_data["tool"]["metadata"]["full_description"]


class Settings(BaseSettings):
    environment: Environments = Environments.PROD
    logging_level: str = "INFO"
    root_path: str = ""
    ci: bool = False
    mongo_uri: str
    mongo_db: str
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_password: str
    jwt_secret_key: str
    ip_rate_limit_per_minute: int = 100
    access_token_expire_minutes: int = 3600

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
