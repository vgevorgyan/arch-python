from ..config import config
from ..constants import CPU
from ..helpers.utils import (debug, get_cpu, is_lvm2_exists,
                             run_command_with_output)


def install_base_system():
    print("Installing base system ...")
    base_packages = config["general"]["base_packages"]
    match get_cpu():
        case CPU.Intel:
            base_packages += " intel-ucode "
        case CPU.AMD:
            base_packages += " amd-ucode "

    if is_lvm2_exists():
        base_packages += " lvm2 "

    debug(base_packages)

    run_command_with_output(
        "pacstrap -K /mnt " + base_packages,
        shell = True,
    )
