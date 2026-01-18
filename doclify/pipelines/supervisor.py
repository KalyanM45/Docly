import click
from doclify.components.init import init_project

@click.group()
def cli():
    pass

@cli.command()
def init():
    init_project()

@cli.command()
def run():
    from doclify.components.run import run_docs
    run_docs()

@cli.command()
@click.argument('path', type=click.Path(exists=True), required=True)
def update(path):
    from doclify.components.update import update_docs
    update_docs(path)