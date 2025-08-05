import tomllib

from .constants import DiskAction


def load_config(file_name):
    with open(file_name, "rb") as f:
        config = tomllib.load(f)

    return config


def config_disks_action():
    if config["disks"]["action"] == "create":
        return DiskAction.Create
    else:
        return DiskAction.Mount


config = load_config("config.toml")
