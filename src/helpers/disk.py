from ..config import config
import subprocess


def disks():
    result = subprocess.run(["lsblk"], capture_output=True, text=True)
    print(result.stdout)


def get_luks_partition():
    partitions = config["disks"]["partitions"]
    for partition in partitions:
        if partition["type"] == "luks-lvm2":
            return partition["partition"]

    return None
