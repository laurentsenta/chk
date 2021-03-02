"""
Deals with configuration.
"""
from pathlib import Path
from os import path, makedirs
import yaml
from datetime import datetime

HOME = str(Path.home())
CONFIG_FOLDER = path.join(HOME, '.chk')
CONFIG_ALIAS = path.join(CONFIG_FOLDER, 'aliases.yaml')
CONFIG_SYNC_LIST = path.join(CONFIG_FOLDER, 'syncs.yaml')

try:
    makedirs(CONFIG_FOLDER)
except FileExistsError as e:
    pass


def log_sync(src: str, destination: str):
    try:
        with open(CONFIG_SYNC_LIST, 'r') as f:
            y = yaml.safe_load(f)

            if src not in y:
                y[src] = {destination: datetime.now()}
            else:
                y[src][destination] = datetime.now()

        with open(CONFIG_SYNC_LIST, 'w') as f:
            return yaml.dump(y, f)
    except FileNotFoundError:
        return {}


def load_aliases():
    try:
        with open(CONFIG_ALIAS, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}


def save_aliases(a):
    with open(CONFIG_ALIAS, 'w') as f:
        return yaml.dump(a, f)


def set_alias(name, p):
    # if not name.isalnum():
    #     raise ValueError('name is not alphanumeric')

    a = load_aliases()
    a[name] = path.abspath(p)
    save_aliases(a)


def unset_alias(name):
    a = load_aliases()
    if name not in a:
        raise IndexError('alias does not exists')
    del a[name]
    save_aliases(a)
