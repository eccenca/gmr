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


def loadParams() -> None:
    """Load the default parameters from conf.yaml file."""
    with open(imr_dir + "/config.yaml") as stream:
        imrConfig = yaml.safe_load(stream)


@click.group()
def cli() -> None:
    """Get the cli command options."""
    #    loadParams()


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
@click.argument("model_directory")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
def push(model_directory: str, package: str, version: str) -> None:
    """Push model to remote repository."""
    imr_remote.push(model_directory, package, version)


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
def pull(package: str, dir: str, version: str) -> None:
    """Pull model from remote repository."""
    imr_remote.pull(dir, package, version)


if __name__ == "__main__":
    cli()
