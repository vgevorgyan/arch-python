from ..config import config_disks_action
from ..constants import DiskAction


def __create_partitions():
    print("Not implemented yet")

def __mount_partitions():
    print("Not implemented yet")

def partitioning():
    match config_disks_action():
        case DiskAction.Create:
            __create_partitions()
        case DiskAction.Mount:
            __mount_partitions()
