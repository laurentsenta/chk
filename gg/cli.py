#!./venv/bin/python

import click
from .config import set_alias, unset_alias, load_aliases


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)


@cli.command()
@click.argument('src')
@click.argument('dst')
def add():
    """Add a module from SRC to DST."""
    pass


@cli.command()
def pull():
    """Pull all changes."""
    pass


@cli.command()
def push():
    """Push back all changes."""
    pass


@cli.group()
def alias():
    pass


@alias.command()
@click.argument('path')
@click.argument('name')
def add(path, name):
    """Alias a PATH to a simpler NAME."""
    set_alias(name, path)


@alias.command()
@click.argument('name')
def rm(name):
    """Remove the alias NAME."""
    unset_alias(name)


@alias.command()
def ls():
    """List all aliases."""
    a = load_aliases()

    for k, v in a.items():
        print(f'{k:<12} ->\t{v:<20}')
