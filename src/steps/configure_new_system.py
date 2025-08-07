from ..config import config
from ..helpers.utils import run_chroot_command, run_chroot_command_with_output


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
    run_chroot_command_with_output(
        ["sed", "-i", "'/en_US.UTF-8/s/^#//g'", "/etc/locale.gen"]
    )
    run_chroot_command_with_output(["locale-gen"])
    run_chroot_command_with_output(
        'echo "LANG=en_US.UTF-8" > /etc/locale.conf', shell=True
    )
    run_chroot_command_with_output(
        'echo "LANGUAGE=en_US" > /etc/locale.conf', shell=True
    )
    run_chroot_command_with_output('echo "LC_ALL=C" > /etc/locale.conf', shell=True)
    run_chroot_command_with_output(
        'echo "' + hostname + '" > /etc/hostname', shell=True
    )
    run_chroot_command_with_output(
        'echo "127.0.0.1    localhost" > /etc/hosts', shell=True
    )
    run_chroot_command_with_output('echo "::1    localhost" > /etc/hosts', shell=True)
    run_chroot_command_with_output(
        'echo "127.0.1.1    '
        + hostname
        + ".localdomain  "
        + hostname
        + '" > /etc/hosts',
        shell=True,
    )
