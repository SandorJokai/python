import click
from infra_tool.logs.log_analyzer import show_logs
from infra_tool.services.systemd import service_check
from infra_tool.monitoring.status import cpu_display
from infra_tool.utils.backup import create_backup, cleanup_backup


@click.group()
def cli():
    """A simple CLI to check system status, restart failed services, check logs and create backups"""
    pass


@cli.command()
@click.option("--last-hour", is_flag=True)
def logs(last_hour):
    """Show service restarts from the journal."""
    show_logs(last_hour=last_hour)


@cli.command()
#@click.argument("service")
def services():
    """Restart a systemd service if failed"""
    service_check()


@cli.command()
@click.argument("action", type=click.Choice(["create", "cleanup"]))
@click.option("--older-than-days", type=int, help="Remove backups older than N days")
def backup(action, older_than_days):
    """Create or cleanup backups"""
    if action == "cleanup":
        if older_than_days is not None:
            cleanup_backup(older_than_days=older_than_days)
        else:
            print("Usage: backup cleanup --older-than-days N(integer) -> cleanup everyting that are older than N day(s).")
    else:
        create_backup()


@cli.command()
def status():
    """Show system status"""
    print("#" * 27)
    print(" System Health Monitoring")
    print("#" * 27)
    print()
    cpu_display()


if __name__ == "__main__":
    cli()
