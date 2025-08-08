#!/bin/env python

from .config import config
from .helpers.network import is_connected
from .helpers.utils import run_command
from .steps.configure_new_system import configure_new_system
from .steps.install_base_system import install_base_system
from .steps.kernel_configuration import kernel_configuration
from .steps.partitioning import partitioning
from .steps.user_configuration import user_configuration

# TODO:  1. Validate config files

# TODO: General - timezone, base system packages, drivers, desktop, username, home folder, groups
# TODO: Disks - partitions
# TODO: Network - hostname, network config (IP, netmask, gateway or DHCP)

# TODO:  2. Check Internet access for installation

print("Checking network connection ...")
if not is_connected():
    raise SystemExit("No internet connection. Please configure your network.")

# TODO:  3. Configure NTP

print("Enabling NTP ...")
run_command(["timedatectl", "set-ntp", "true"])
print("Setting timezone ...")
run_command(["timedatectl", "set-timezone", config["general"]["timezone"]])

# TODO:  4. Partitioning

partitioning()

# TODO:  5. Install base system

install_base_system()

# TODO:  6. Configure new system timezone, clock, locale and hosts

configure_new_system()

# TODO:  7. User configuration

user_configuration()

# TODO:  8. fstab generation

run_command("genfstab -pU /mnt >> /mnt/etc/fstab", shell=True)

# TODO:  9. Kernel configuration and grub installation

kernel_configuration()

# TODO: 10. Drivers installation
# TODO: 11. Desktop environment installation and configuration
# TODO: 12. Additional packages installation
