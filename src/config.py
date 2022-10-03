from contextlib import suppress
from functools import lru_cache

import requests
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Settings"""

    # App
    app_name: str

    # Logging
    logging_level_stdout: str = "debug"

    # Google
    project_id: str | None = None

    class Config:
        """Settings config"""

        env_file = ".env"
        # env_prefix = "<some_prefix>"


@lru_cache()
def get_config() -> Settings:
    """Return cached settings"""

    # Try to get the Google project ID from the Google cloud environment
    with suppress(requests.exceptions.ConnectionError):
        response = requests.get(
            url="http://metadata.google.internal/computeMetadata/v1/project/project-id",
            headers={"Metadata-Flavor": "Google"},
        )

        if response.status_code == 200:
            Settings.project_id = response.text

    return Settings()


__all__ = ["get_config"]
