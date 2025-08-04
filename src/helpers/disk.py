import subprocess


def disks():
    result = subprocess.run(["lsblk"], capture_output=True, text=True)
    print(result.stdout)
