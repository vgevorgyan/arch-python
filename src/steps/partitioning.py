from src.helpers.utils import run_command, run_command_with_output

from ..config import config, config_disks_action, config_partition_type
from ..constants import DiskAction, PartitionType


def __create_partitions():
    print("Not implemented yet")

def __mount_efi_partition(partition):
    if partition["format"]:
        run_command_with_output(["mkfs.fat", "-F32", partition["partition"]])


def __mount_swap_partition(partition):
    print("Creating and mounting swap partition.")
    run_command(["mkswap", partition["partition"]])
    run_command(["swapon", partition["partition"]])

def __mount_partitions():
    for partition in config["disks"]["partitions"]:
        match config_partition_type(partition["type"]):
            case PartitionType.Efi:
                __mount_efi_partition(partition)
            case PartitionType.Swap:
                __mount_swap_partition(partition)

def partitioning():
    print("Partitioning ...")
    match config_disks_action():
        case DiskAction.Create:
            __create_partitions()
        case DiskAction.Mount:
            __mount_partitions()
