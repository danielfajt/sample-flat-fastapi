import click


@click.group()
def app():
    """Application CLI"""


@app.command()
def hello():
    """Hello world command"""
