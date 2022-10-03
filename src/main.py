import typer
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api import api_router
from cli import cli
from config import get_config
from logger import logger

app_config = get_config()


# FastAPI: Config
api = FastAPI(
    title="My application title",
    description="My application description",
    version="0.0.1",
)

# FastAPI: Router
api.include_router(api_router)


# FastAPI: Health check
@api.get("/", tags=["App"])
def info():
    """Index endpoint"""
    return {"Application name": app_config.app_name}


# CLI: Entrypoint
entrypoint = typer.Typer(add_completion=False, no_args_is_help=True)

# CLI
entrypoint.add_typer(cli, name="cli")


if __name__ == "__main__":
    entrypoint()
