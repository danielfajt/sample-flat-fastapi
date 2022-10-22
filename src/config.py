from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

from pyproject import __description, __name, __version

load_dotenv()


class Settings(BaseSettings):
    """Settings"""

    # App
    app_version: str = __version
    app_name: str = __name
    app_description: str = __description

    # Logging
    logging_level_stdout: str = "debug"

    class Config:
        """Settings config"""

        env_file = ".env"
        env_prefix = "APP"


@lru_cache()
def get_config() -> Settings:
    """Return cached settings"""

    return Settings()


__all__ = ["get_config"]
