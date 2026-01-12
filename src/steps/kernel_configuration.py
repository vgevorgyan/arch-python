from ..helpers.disk import (get_luks_partition, get_partition_uuid)
from ..helpers.utils import (
    edit_file_regexp,
    install_packages,
    is_lvm2_exists,
    run_chroot_command_with_output,
    run_command,
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
    run_command('echo "KEYMAP=us" > /mnt/etc/vconsole.conf', shell=True)
    run_command('echo "FONT=lat9w-16" >> /mnt/etc/vconsole.conf', shell=True)
    run_chroot_command_with_output(["mkinitcpio", "-P"])
    install_packages(
        ["grub", "efibootmgr", "dosfstools", "os-prober", "mtools"])
    run_chroot_command_with_output(
        [
            "grub-install",
            "--target=x86_64-efi",
            "--efi-directory=/boot/efi",
            "--bootloader-id=PlagueLinux",
            "--recheck",
        ]
    )
    luks_partition = get_luks_partition()
    if luks_partition is None:
        raise SystemExit("No luks partition")
    luks_uuid = get_partition_uuid(luks_partition)
    edit_file_regexp(
        "/mnt/etc/default/grub",
        r"^GRUB_CMDLINE_LINUX=",
        'GRUB_CMDLINE_LINUX=""',
        'GRUB_CMDLINE_LINUX="cryptdevice=UUID='
        + luks_uuid
        + ":cryptlvm "
        + 'root=/dev/system/root"',
    )
    edit_file_regexp(
        "/mnt/etc/default/grub",
        r"^#GRUB_ENABLE_CRYPTODISK=",
        '#GRUB_ENABLE_CRYPTODISK=y',
        'GRUB_ENABLE_CRYPTODISK=y',
    )
    run_chroot_command_with_output(
        ["grub-mkconfig", "-o", "/boot/grub/grub.cfg"])
