from ..config import config, config_disks_action, config_partition_type
from ..helpers.utils import (
    edit_file_regexp,
    install_packages,
    is_lvm2_exists,
    run_chroot_command,
    run_chroot_command_with_output,
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
    run_chroot_command_with_output(["mkinitcpio", "-P"])
    install_packages(
        ["grub", "efibootmgr", "dosfstools", "os-prober", "mtools"])
    edit_file_regexp(
        "/mnt/etc/default/grub",
        r"^GRUB_CMDLINE_LINUX=",
        "GRUB_CMDLINE_LINUX=",
        'GRUB_CMDLINE_LINUX="cryptdevice=/dev/vda4:cryptlvm root=/dev/system/root"',
    )
    run_chroot_command_with_output(
        ["grub-mkconfig", "-o", "/boot/grub/grub.cfg"])
