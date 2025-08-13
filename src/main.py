#!/bin/env python

from .config import config
from .helpers.network import is_connected
from .helpers.utils import edit_file, install_packages, run_command
from .steps.configure_new_system import configure_new_system
from .steps.install_base_system import install_base_system
from .steps.kernel_configuration import kernel_configuration
from .steps.partitioning import partitioning
from .steps.user_configuration import user_configuration

print("Checking network connection ...")
if not is_connected():
    raise SystemExit("No internet connection. Please configure your network.")

print("Enabling NTP ...")
run_command(["timedatectl", "set-ntp", "true"])
print("Setting timezone ...")
run_command(["timedatectl", "set-timezone", config["general"]["timezone"]])

partitioning()
install_base_system()
configure_new_system()
user_configuration()
run_command("genfstab -pU /mnt >> /mnt/etc/fstab", shell=True)
kernel_configuration()
install_packages(["sudo"])
edit_file(
    "/mnt/etc/sudoers",
    "# %wheel ALL=(ALL:ALL) ALL",
    "# %wheel ALL=(ALL:ALL) ALL",
    "%wheel ALL=(ALL:ALL) ALL",
)
