import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

backup_dest = Path.home()/"infra-tool-backups"


def days_ago_to_epoch(days: int) -> int:
    cutoff = datetime.now() - timedelta(days=days)
    return int(cutoff.timestamp())


def create_backup():
    backup_source = input("Type absolute path to create the backup from: ")

    if not backup_dest.is_dir():
        backup_dest.mkdir()

    if backup_source.endswith("/"):
        backup_source = backup_source.rstrip("/")

    backup_folder = os.path.split(f"{backup_source}")
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive = f"{backup_dest}/{backup_folder[-1]}_{now}.tgz"

    if not os.path.exists(backup_source):
        print(f"\033[5;1;31mBackup source does not exist:\033[0m {backup_source}")

    else:
        try:
            result = subprocess.run(
                    ["sudo", "tar", "-czvf", archive, backup_source],
                    text=True,
                    check=True,
                    capture_output=True
                )
            print(f"Backup has been created from \033[5;1;31m{backup_source}\033[0m to \033[5;1;31m{archive}\033[0m")
        except subprocess.CalledProcessError as err:
            print(f"\033[5;1;31mSomething went wrong during the backup process:\033[0m {err}")


def cleanup_backup(older_than_days: float) -> float:
    cutoff_epoch = days_ago_to_epoch(older_than_days)

    removed_any = False

    for backup in backup_dest.iterdir():
        file_age = subprocess.run(
                ["stat", "-c", "%W", backup],
                text=True,
                check=True,
                capture_output=True
            )

        epoch_str = file_age.stdout.strip()   # Extract text output
        epoch = float(epoch_str)

        if cutoff_epoch >= epoch:
            removed_any = True

            result = subprocess.run(
                    ["rm", "-f", backup],
                    check=True,
                    text=True,
                    capture_output=True
                )
            print(f"Removing \033[5;1;31m{backup.name}\033[0m which is older than {older_than_days} days...")
            print(f"\033[5;1;31m{backup.name}\033[0m removed.")

    if not removed_any:
        print("There's no backup file to be removed.")
