import logging

from config import get_config
from logger_json import JsonStreamHandler

app_config = get_config()

APP_NAME = app_config.app_name
LOGGING_LEVEL = app_config.logging_level_stdout.upper()

# Logger
logger = logging.getLogger("app")
logger.setLevel(LOGGING_LEVEL)

# Logger: Handlers
logger.addHandler(JsonStreamHandler())

# Supress logging from other libraries
logging.getLogger("urllib3").setLevel(logging.ERROR)
