import os
from datetime import datetime

from ..config import config
from ..helpers.utils import run_chroot_command, run_command


def user_configuration():
    username = config["user"]["username"]
    home = config["user"]["home"]

    print("Configuring user ...")
    if os.path.isdir("/mnt" + home):
        print("Home dir exists")
        os.rename(
            "/mnt" + home, "/mnt" + home + "-" + datetime.now().strftime("%Y%m%d%H%M%S")
        )
    else:
        print("Home dir NOT exists")

    # run_chroot_command(["groupadd", "-g", "1000", username])
    # run_chroot_command(["useradd", "-m", "-g", "1000", "-u", "1000", username])
