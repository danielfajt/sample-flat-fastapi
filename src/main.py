import click
import uvicorn
from fastapi import FastAPI

from api import api_router
from cli import app
from config import get_config
from logger import logger

app_config = get_config()


# FastAPI: Config
api = FastAPI(
    title=app_config.app_name,
    description=app_config.app_description,
    version=app_config.app_version,
)

# FastAPI: Router
api.include_router(api_router)


@click.command()
def run():
    """Run FastAPI development server"""

    uvicorn.run(
        "main:api",
        port=5050,
        log_level=app_config.logging_level_stdout,
        reload=True,
        debug=False,
    )


# CLI: Entrypoint
@click.group()
def entry_point():
    f"""{app_config.app_description}"""


entry_point.add_command(app)
entry_point.add_command(run)


if __name__ == "__main__":
    entry_point()
