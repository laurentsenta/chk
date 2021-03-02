#!./venv/bin/python

from typing import DefaultDict
from copier.config.objects import DEFAULT_EXCLUDE
import yaml
from os import makedirs, path, getcwd
from glob import glob

import click
from plumbum import TF, colors, local

from .config import load_aliases, log_sync, set_alias, unset_alias
from copier import copy as _copy

git = local["git"]

CHK_EXCLUDES = tuple([*DEFAULT_EXCLUDE, '.chunk.yaml'])


def load_source(src: str) -> str:
    # TODO: handle git and github repositories
    aliases = load_aliases()

    if src in aliases:
        source = aliases[src]
    else:
        source = path.abspath(src)

    return source


def load_chunk(dst: str):
    destination = path.abspath(dst)
    with open(path.join(destination, ".chunk.yaml"), 'r') as f:
        return yaml.safe_load(f)


def sync_chunk(src: str, destination: str):
    source = load_source(src)

    # if has_changes(source):
    #     raise Exception('Has Changes!')

    with local.cwd(source):
        HEAD = git("rev-parse", "HEAD").strip()

    # store gg metadata in the repo
    with open(path.join(destination, ".chunk.yaml"), 'w') as f:
        yaml.dump(dict(src=src, HEAD=HEAD), f, sort_keys=True, indent=2)

    log_sync(src, destination)


def has_changes(source: str) -> bool:
    with local.cwd(source):
        status = git('status', '-s', './')
        print('status', status)

    return status.strip() != ''


def copy(src, dst):
    source = load_source(src)
    _copy(source, dst, exclude=CHK_EXCLUDES)


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@cli.command()
@click.argument('target', default=None, type=str, required=False)
def ls(target: str):
    """List all chunks in TARGET."""
    # TODO: add "include dotfiles" options to get .x listing too.

    if target is None:
        target = getcwd()
    target = path.abspath(target)

    search = path.join(target, "**", ".chunk.yaml")
    print(search)

    # TODO: find a way to make this usable despite node modules
    files = glob(search, recursive=True)

    mapping = DefaultDict(list)

    for file in files:
        dir = path.dirname(file)
        c = load_chunk(dir)
        src = c["src"]

        mapping[src].append(dir)

        log_sync(src, path.abspath(dir))

    for (k, v) in mapping.items():
        print('*', k)

        for x in v:
            print('\t->', x[len(target) + 1:])



@cli.command()
@click.argument('src')
@click.argument('dst')
def clone(src: str, dst: str):
    """Clone a module from SRC to DST."""
    destination = path.abspath(dst)
    # TODO: replace with false this is just for testing:
    makedirs(destination, exist_ok=True)

    sync_chunk(src, destination)
    copy(src, destination)


@cli.command()
@click.argument('target', default=None, type=str, required=False)
def pull(target):
    """Pull all changes."""
    if target is None:
        target = getcwd()
    target = path.abspath(target)

    dot_chunk = load_chunk(target)
    src = dot_chunk["src"]
    source = load_source(src)

    sync_chunk(src, target)
    copy(source, target)


@cli.command()
@click.argument('target', default=None, type=str, required=False)
def push(target):
    """Push back all changes."""
    if target is None:
        target = getcwd()

    target = path.abspath(target)

    dot_chunk = load_chunk(target)
    src = dot_chunk["src"]
    source = load_source(src)

    copy(target, source)


@cli.group()
def alias():
    pass


@alias.command()
@click.argument('folder')
@click.argument('name')
def add(folder, name):
    """Alias a PATH to a simpler NAME."""
    target = path.abspath(folder)

    if not path.exists(target):
        raise FileNotFoundError(target)

    set_alias(name, target)


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
