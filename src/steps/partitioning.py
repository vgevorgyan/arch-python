from ..config import config, config_disks_action
from ..constants import DiskAction


def __create_partitions():
    print("Not implemented yet")

def __mount_partitions():
    for partition in config["disks"]["partitions"]:
        print(partition)
    print("Not implemented yet")

def partitioning():
    print("Partitioning ...")
    match config_disks_action():
        case DiskAction.Create:
            __create_partitions()
        case DiskAction.Mount:
            __mount_partitions()
