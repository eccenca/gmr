from pathlib import Path
""" Path module.

For handling local files and directory operations.
"""

import click
import yaml

from imr import IMRLocal, IMRRemote

home = Path.home()
imr_dir = home + "/.imr"
imr_local: IMRLocal = IMRLocal(imr_dir)
imr_remote: IMRRemote = None
imr_config = None

def load_params() -> None:
    """Load the default parameters from conf.yaml file."""
    with Path.open(imr_dir + "/config.yaml") as stream:
        imr_config = yaml.safe_load(stream)


@click.group()
def cli() -> None:
    """Get the cli command options."""
    #  add  loadParams() later


@cli.group()
def local() -> None:
    """Get local command options."""


@local.command("list")
def list_local() -> None:
    """List local packages."""
    for package in imr_local.list():
        print(package)


@local.command()
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
def remove(package: str, version: str) -> None:
    """Remove local packages."""
    local.rm(package, version)


@cli.group()
@click.argument("host")
@click.argument("user")
@click.argument("password")
def remote(host: str, user: str, password: str) -> None:
    """Get remote command cli options."""
    global imr_remote
    imr_remote = IMRRemote(host, user, password)


@remote.command("list")
def list_remote() -> None:
    """List remote packages."""
    packages = imr_remote.list()
    for p in packages:
        print(p)


@remote.command()
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
def rm(package: str, version: str) -> None:
    """Remove remote package."""
    imr_remote.rm(package, version)


@remote.command()
@click.argument("model_dir")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
def push(model_dir: str, package: str, version: str) -> None:
    """Push model to remote repository."""
    imr_remote.push(model_dir, package, version)


@remote.command()
@click.argument("package")
@click.option(
    "-d",
    "--dir",
    type=str,
    default=imr_dir,
    help="directory to pull the model in.",
    show_default=True,
)
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
def pull(package: str, model_dir: str, version: str) -> None:
    """Pull model from remote repository."""
    imr_remote.pull(model_dir, package, version)


if __name__ == "__main__":
    cli()
