import tomllib

from .constants import DiskAction, PartitionType


def load_config(file_name):
    with open(file_name, "rb") as f:
        config = tomllib.load(f)

    return config


def config_disks_action():
    if config["disks"]["action"] == "create":
        return DiskAction.Create
    else:
        return DiskAction.Mount


def config_partition_type(type):
    match type:
        case "efi":
            return PartitionType.Efi
        case "boot":
            return PartitionType.Boot
        case "swap":
            return PartitionType.Swap
        case "luks-lvm2":
            return PartitionType.LuksLvm2


config = load_config("config.toml")
