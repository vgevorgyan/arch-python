from ..config import config, config_disks_action, config_partition_type
from ..helpers.utils import (
    edit_file_regexp,
    is_lvm2_exists,
    run_chroot_command,
    run_command,
    run_command_with_output,
)


def kernel_configuration():
    packages = " encrypt filesystems "
    if is_lvm2_exists():
        packages = " encrypt lvm2 filesystems "

    edit_file_regexp(
        "/mnt/etc/mkinitcpio.conf",
        r"^HOOKS=",
        " filesystems ",
        packages,
    )
