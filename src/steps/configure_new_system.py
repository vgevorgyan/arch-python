from ..config import config
from ..helpers.utils import (
    edit_file,
    run_chroot_command,
    run_chroot_command_with_output,
    run_command,
)


def configure_new_system():
    hostname = config["network"]["hostname"]
    run_chroot_command(
        [
            "ln",
            "-sf",
            "/usr/share/zoneinfo/" + config["general"]["timezone"],
            "/etc/localtime",
        ]
    )
    run_chroot_command_with_output(["hwclock", "--systohc"])
    run_command("sed -i '/en_US.UTF-8/s/^#//g' /mnt/etc/locale.gen")
    edit_file("/mnt/etc/locale.gen", "en_US.UTF-8", "#en_US.UTF-8", "en_US.UTF-8")
    run_chroot_command_with_output(["locale-gen"])
    run_command('echo "LANG=en_US.UTF-8" > /mnt/etc/locale.conf', shell=True)
    run_command('echo "LANGUAGE=en_US" >> /mnt/etc/locale.conf', shell=True)
    run_command('echo "LC_ALL=C" >> /mnt/etc/locale.conf', shell=True)
    run_command('echo "' + hostname + '" > /mnt/etc/hostname', shell=True)
    run_command('echo "127.0.0.1    localhost" > /mnt/etc/hosts', shell=True)
    run_command('echo "::1    localhost" >> /mnt/etc/hosts', shell=True)
    run_command(
        'echo "127.0.1.1    '
        + hostname
        + ".localdomain  "
        + hostname
        + '" >> /mnt/etc/hosts',
        shell=True,
    )
