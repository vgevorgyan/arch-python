#!/bin/env python

from .helpers.network import is_connected
from .helpers.utils import load_config

# TODO:  1. Validate config files
config = load_config("config.toml")

# TODO: General - timezone, base system packages, drivers, desktop, username, home folder, groups
# TODO: Disks - partitions
# TODO: Network - hostname, network config (IP, netmask, gateway or DHCP)

# TODO:  2. Configure Internet access for installation

if not is_connected():
    raise SystemExit("No internet connection. Please configure your network.")

# TODO:  3. Configure NTP
# TODO:  4. Partitioning
# TODO:  5. Install base system
# TODO:  6. Configure new system timezone, clock, locale and hosts
# TODO:  7. User configuration
# TODO:  8. fstab generation
# TODO:  9. Kernel configuration and grub installation
# TODO: 10. Drivers installation
# TODO: 11. Desktop environment installation and configuration
# TODO: 12. Additional packages installation
