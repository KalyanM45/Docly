import click
from docly.init import init_project

@click.group()
def cli():
    pass

@cli.command()
@click.option("--force", is_flag=True)
@click.option("--python", is_flag=True, help="Use Python gitignore")
def init(force, python):
    ignore_name = "Python" if python else None
    init_project(force, ignore_name)

if __name__ == "__main__":
    cli()