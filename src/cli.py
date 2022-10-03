import asyncio
import json
import logging

import typer

logger = logging.getLogger("app.cli")

cli = typer.Typer(no_args_is_help=True)

# Run event loop to run commands coroutines with
loop = asyncio.get_event_loop()


@cli.command(name="hello")
def get_hello(icao: str) -> None:
    """Get hello"""

    # response = loop.run_until_complete(<coroutine>) >>> async  method from 'controller'

    typer.secho(f'\nHello', fg="green")
    loop.close()
