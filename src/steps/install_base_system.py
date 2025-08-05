from ..config import config
from ..constants import CPU
from ..helpers.utils import debug, get_cpu, run_command_with_output


def _should_install_lvm2():
    for partition in config["disks"]["partitions"]:
        if "lvm2" in partition["type"]:
            return True


def install_base_system():
    print("Installing base system ...")
    base_packages = config["general"]["base_packages"]
    match get_cpu():
        case CPU.Intel:
            base_packages += " intel-ucode "
        case CPU.AMD:
            base_packages += " amd-ucode "

    if _should_install_lvm2():
        base_packages += " lvm2 "

    debug(base_packages)

    run_command_with_output(
        "pacstrap -K /mnt " + base_packages,
        shell = True,
    )
