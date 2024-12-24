import click
from dynaconf import settings

from driink.notifier import notify
import driink.config as u_config


user_config = u_config.load_user_config()


@click.group()
def cli():
    """A command-line tool to track water consumption and remind you to stay
    hydrated.
    """
    pass


# 'drank' Command
@cli.command()
@click.option("--amount", required=True, type=int, help="Amount of water in ml to log.")
def drank(amount):
    """Log the amount of water you drank."""
    if not u_config.validate():
        print("the configuration is not valid")
        return

    # add_water(amount)
    msg = f"Logged {amount}ml of water."
    click.echo(msg)
    notify(msg)


# 'config' Command
@cli.command()
@click.option("--key", required=False, help="Setting name to change")
@click.option("--value", required=False, help="Setting value to change")
def config(key, value):
    """Change configuration settings"""
    if key is None or value is None:
        u_config.present_config()
        return

    if u_config.set_config_param(key, value):
        message = "setting changed successfully"
    else:
        message = "error changing the settings"

    click.echo(message)
    notify(message)


def main():
    cli()


if __name__ == "__main__":

    cli()
