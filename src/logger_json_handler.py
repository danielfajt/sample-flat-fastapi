import sys
import typing as t
from logging import LogRecord, StreamHandler
from webbrowser import get

from config import get_config

app_config = get_config()


class JsonStreamHandler(StreamHandler):
    """Print logging message to STDOUT in JSON format."""

    def __init__(self):
        super().__init__(stream=sys.stdout)
        self.app_name = app_config.app_name

    def emit(self, record: LogRecord) -> None:
        """
        Change logging message to structured object.
        """

        new_msg: dict[str, t.Any] = {}

        if isinstance(record.msg, str):
            new_msg = {"message": record.msg}

        # If the record.msg is type dict, merge original with new
        if isinstance(record.msg, dict):
            new_msg = {**record.msg, **new_msg}

        new_msg["severity"] = record.levelname

        # Force to empty buffers.
        # This should be handled globally in Dockerfile with 'ENV PYTHONUNBUFFERED True'
        sys.stdout.flush()

        # Convert msg back to str
        record.msg = str(new_msg)
        super().emit(record)

    def format(self, record: LogRecord) -> str:
        """Replace single quotes with double quotes.

        * Standard output uses single quotes which is not a JSON format.

        Args:
            record: Logging record
        """

        return super().format(record).replace("'", '"')
