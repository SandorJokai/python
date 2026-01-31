from .monitoring.status import cpu_display
from .services.systemd import service_check
from .logs.log_analyzer import show_logs
from .utils.backup import create_backup, cleanup_backup


def main():
    print("Main script starting...")
    cpu_display()
    service_check()
    show_logs()
    create_backup()
    cleanup_backup()

