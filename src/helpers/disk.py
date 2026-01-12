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


def get_partition_uuid(partition_path):
    """
    Get the UUID of a partition by its device path.
    
    Args:
        partition_path: Path to the partition device (e.g., '/dev/sda1')
    
    Returns:
        str: UUID of the partition, or None if not found or error occurred
    """
    try:
        result = subprocess.run(
            ["blkid", "-s", "UUID", "-o", "value", partition_path],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        return None
    except (subprocess.SubprocessError, FileNotFoundError):
        return None
