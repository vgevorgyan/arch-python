import random
import re
import string
import subprocess

from ..config import config
from ..constants import CPU


def run_command(command, shell=False):
    result = subprocess.run(
        command,
        capture_output=True,
        shell=shell,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip())
    return result.stdout.strip()


def run_chroot_command(command, shell=False):
    if isinstance(command, list):
        command = ["arch-chroot", "/mnt"] + command
    else:
        command = "arch-chroot /mnt " + command

    result = subprocess.run(
        command,
        capture_output=True,
        shell=shell,
        text=True,
    )

    return result.stdout.strip()


def run_chroot_command_with_output(command, shell=False):
    if isinstance(command, list):
        command = ["arch-chroot", "/mnt"] + command
        print("Running command: " + " ".join(command))
    else:
        command = "arch-chroot /mnt " + command
        print("Running command: " + command)

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=shell,
        text=True,
    )
    if process.stdout is not None:
        for line in process.stdout:
            print(line, end="")


def run_command_with_output(command, shell=False, show_output=True):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=shell,
        text=True,
    )
    if process.stdout is not None:
        for line in process.stdout:
            if show_output:
                print(line, end="")


def get_cpu():
    cpu_vendor = run_command(["lscpu | grep Vendor"], shell=True).lower()
    if "intel" in cpu_vendor:
        return CPU.Intel
    if "amd" in cpu_vendor:
        return CPU.AMD


def random_string(length=12):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def debug(message):
    if config["general"]["debug"]:
        print(message)


def is_lvm2_exists():
    for partition in config["disks"]["partitions"]:
        if "lvm2" in partition["type"]:
            return True


def edit_file(file_path, find, replace, to):
    with open(file_path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if find in line:
            lines[i] = line.replace(replace, to)

    with open(file_path, "w") as f:
        f.writelines(lines)


def edit_file_regexp(file_path, find, replace, to):
    with open(file_path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if re.search(find, line):
            lines[i] = line.replace(replace, to)

    with open(file_path, "w") as f:
        f.writelines(lines)


def install_packages(packages):
    command = ["pacman", "-Sy", "--noconfirm"] + packages
    run_chroot_command_with_output(command)


def install_packages_new_system(packages):
    command = ["sudo", "pacman", "-Sy", "--needed", "--noconfirm"] + packages
    run_command_with_output(command)
