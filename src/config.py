from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

from pyproject import __description__, __name__, __version__

load_dotenv()


class Settings(BaseSettings):
    """Settings"""

    # App
    app_version: str = __version__
    app_name: str = __name__
    app_description: str = __description__

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
