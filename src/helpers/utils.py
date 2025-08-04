import random
import string
import subprocess
import sys
import tomllib

from ..constants import CPU


def load_config(file_name):
    with open(file_name, "rb") as f:
        config = tomllib.load(f)

    return config


def run_command(command, shell=False):
    result = subprocess.run(
        command,
        capture_output=True,
        shell=shell,
        stdout=sys.stdout,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip())
    return result.stdout.strip()


def get_cpu():
    cpu_vendor = run_command(["lscpu | grep Vendor"], shell=True).lower()
    if "intel" in cpu_vendor:
        return CPU.Intel
    if "amd" in cpu_vendor:
        return CPU.AMD


def random_string(length=12):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))
