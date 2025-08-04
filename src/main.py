#!/bin/env python

from src.constants import CPU

from .helpers.network import is_connected
from .helpers.utils import get_cpu, load_config, run_command

# TODO:  1. Validate config files
config = load_config("config.toml")

is_debug = config["general"]["debug"]

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
run_command(["timedatectl", "set-timezone", config["general"]["timezone"]], shell=True)

# TODO:  4. Partitioning
# TODO:  5. Install base system

print("Installing base system ...")
base_packages = config["general"]["base_packages"]
match get_cpu():
    case CPU.Intel:
        base_packages += " intel-ucode"
    case CPU.AMD:
        base_packages += " amd-ucode"

if is_debug:
    print(base_packages)

run_command(
    "pacstrap -K /mnt " + base_packages,
    shell=True,
)

# TODO:  6. Configure new system timezone, clock, locale and hosts
# TODO:  7. User configuration
# TODO:  8. fstab generation
# TODO:  9. Kernel configuration and grub installation
# TODO: 10. Drivers installation
# TODO: 11. Desktop environment installation and configuration
# TODO: 12. Additional packages installation
