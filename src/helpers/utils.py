import random
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


def run_command_with_output(command, shell=False, show_output=True):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=shell,
        text=True,
    )
    if process.stdout != None and show_output:
        for line in process.stdout:
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
