import pathlib

import tomllib
from pydantic_settings import BaseSettings, SettingsConfigDict

path = pathlib.Path(__file__).parent.absolute()
with open(f"{path}/../pyproject.toml", mode="rb") as f:
    project_data = tomllib.load(f)

app_version = project_data["tool"]["poetry"]["version"]
app_name = project_data["tool"]["poetry"]["name"]
app_title = project_data["tool"]["metadata"]["title"]
app_description = project_data["tool"]["metadata"]["full_description"]


class Settings(BaseSettings):
    environment: str = "production"
    logging_level: str = "INFO"
    root_path: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
