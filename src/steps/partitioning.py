from ..config import config, config_disks_action, config_partition_type
from ..constants import DiskAction, PartitionType
from ..helpers.utils import run_command, run_command_with_output


def __create_partitions():
    print("Not implemented yet")

def __mount_boot_partition(partition):
    if partition["format"]:
        response = input("Are you sure that you want to format " + partition["partition"] + "partition?").strip().lower()
        if (response == "y"):
            run_command_with_output(["mkfs.fat", "-F32", partition["partition"]])
    run_command_with_output(["mount", "--mkdir", partition["partition"], "/mnt/boot"])

def __mount_efi_partition(partition):
    if partition["format"]:
        response = input("Are you sure that you want to format " + partition["partition"] + "partition?").strip().lower()
        if (response == "y"):
            run_command_with_output(["mkfs.fat", "-F32", partition["partition"]])
    run_command_with_output(["mount", "--mkdir", partition["partition"], "/mnt/boot/efi"])


def __mount_swap_partition(partition):
    print("Creating and mounting swap partition...")
    run_command(["mkswap", partition["partition"]])
    run_command(["swapon", partition["partition"]])

def __mount_luks_lvm2_partitions(partition):
    name = partition["name"]
    crypt_name = partition["crypt_name"]
    password = partition["password"]
    part = partition["partition"]
    run_command_with_output("echo -n '" + password + "' | cryptsetup open" + part + " " + crypt_name, shell=True)
    for lvm_partition in config["disks"][name]["partitions"]:
        lvm_name = lvm_partition["name"]
        mount = lvm_partition["mount"]
        format = lvm_partition["format"]
        lvm_device = "/dev/" + name + "/" + lvm_name
        if format:
            response = input("Are you sure that you want to format " + lvm_device + "partition?").strip().lower()
            if (response == "y"):
                run_command_with_output(["mkfs.ext4", lvm_device])
        run_command_with_output(["mount", "--mkdir", lvm_device, "/mnt" + mount])

def __mount_partitions():
    for partition in config["disks"]["partitions"]:
        match config_partition_type(partition["type"]):
            case PartitionType.Efi:
                __mount_efi_partition(partition)
            case PartitionType.Boot:
                __mount_boot_partition(partition)
            case PartitionType.Swap:
                __mount_swap_partition(partition)
            case PartitionType.LuksLvm2:
                __mount_luks_lvm2_partitions(partition)

def partitioning():
    print("Partitioning ...")
    match config_disks_action():
        case DiskAction.Create:
            __create_partitions()
        case DiskAction.Mount:
            __mount_partitions()
