from os.path import expanduser

import click
import yaml

from imr import IMRLocal, IMRRemote

home = expanduser("~")
imr_dir = home + "/.imr"
imr_local: IMRLocal = IMRLocal(imr_dir)
imr_remote: IMRRemote = None


def loadParams() -> None:
    with open(imr_dir + "/config.yaml") as stream:
        imrConfig = yaml.safe_load(stream)


@click.group()
def cli() -> None:
    #    loadParams()
    pass


@cli.group()
def local() -> None:
    pass


@local.command()
def list_local() -> None:
    for package in imr_local.list():
        print(package)


@local.command()
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
def remove(package: str, version: str) -> None:
    list = local.rm(package, version)


@cli.group()
@click.argument("host")
@click.argument("user")
@click.argument("password")
def remote(host: str, user: str, password: str) -> None:
    global imr_remote
    imr_remote = IMRRemote(host, user, password)


@remote.command()
def list_remote() -> None:
    list = imr_remote.list()
    for p in list:
        print(p)


@remote.command()
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
def rm(package: str, version: str) -> None:
    imr_remote.rm(package, version)


@remote.command()
@click.argument("model_directory")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
def push(model_directory: str, package: str, version: str) -> None:
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
def pull(package :str, dir :str, version :str) -> None:
    imr_remote.pull(dir, package, version)


if __name__ == "__main__":
    cli()
