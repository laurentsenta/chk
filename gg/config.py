"""
Deals with configuration.
"""
from pathlib import Path
from os import path, makedirs
import json

HOME = str(Path.home())
CONFIG_FOLDER = path.join(HOME, '.gg')
CONFIG_ALIAS = path.join(CONFIG_FOLDER, 'aliases.json')

try:
    makedirs(CONFIG_FOLDER)
except FileExistsError as e:
    pass


def load_aliases():
    try:
        with open(CONFIG_ALIAS, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_aliases(a):
    with open(CONFIG_ALIAS, 'w') as f:
        return json.dump(a, f)


def set_alias(name, path):
    if not name.isalnum():
        raise ValueError('name is not alphanumeric')

    a = load_aliases()
    a[name] = path
    save_aliases(a)


def unset_alias(name):
    a = load_aliases()
    if name not in a:
        raise IndexError('alias does not exists')
    del a[name]
    save_aliases(a)
