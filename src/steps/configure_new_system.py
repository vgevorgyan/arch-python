from ..config import config
from ..helpers.utils import (
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
    # run_chroot_command_with_output(
    #     ["sed", "-i", "'/en_US.UTF-8/s/^#//g'", "/etc/locale.gen"]
    # )
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
