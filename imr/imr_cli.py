"""Path module.

For handling local files and directory operations.
"""

from pathlib import Path

import click

from imr.imr import IMRLocal, IMRRemote


class Context:
    """The context for all CLI commands."""

    home = Path.home()
    imr_dir = home / ".imr"
    imr_local: IMRLocal = IMRLocal(str(imr_dir))
    imr_remote: IMRRemote


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Get the cli command options."""
    ctx.obj = Context()
    #  add  loadParams() later


@cli.group()
def local() -> None:
    """Get local command options."""


@local.command("list")
@click.pass_obj
def list_local(obj: Context) -> None:
    """List local packages."""
    for package in obj.imr_local.list():
        click.echo(package)


@local.command("rm")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def rm_local(obj: Context, package: str, version: str) -> None:
    """Remove local packages."""
    obj.imr_local.rm(package, version)


@local.command("path")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def path_local(obj: Context, package: str, version: str) -> None:
    """Get remote model path."""
    click.echo(obj.imr_local.path(package, version))


@cli.group()
@click.argument("host")
@click.argument("user")
@click.argument("password")
@click.pass_obj
def remote(obj: Context, host: str, user: str, password: str) -> None:
    """Get remote command cli options."""
    obj.imr_remote = IMRRemote(host, user, password)


@remote.command("list")
@click.pass_obj
def list_remote(obj: Context) -> None:
    """List remote packages."""
    packages = obj.imr_remote.list()
    for p in packages:
        click.echo(p)


@remote.command("rm")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def rm_remote(obj: Context, package: str, version: str) -> None:
    """Remove remote package."""
    obj.imr_remote.rm(package, version)


@remote.command("push")
@click.argument("model_dir")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def push_remote(obj: Context, model_dir: str, package: str, version: str) -> None:
    """Push model to remote repository."""
    obj.imr_remote.push(model_dir, package, version)


@remote.command()
@click.argument("package")
@click.option(
    "-d",
    "--dir",
    type=str,
    help="directory to pull the model in.",
    show_default=True,
)
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def pull(obj: Context, package: str, model_dir: str, version: str) -> None:
    """Pull model from remote repository."""
    obj.imr_remote.pull(model_dir, package, version)


@remote.command("path")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def path_remote(obj: Context, package: str, version: str) -> None:
    """Get remote model path."""
    click.echo(obj.imr_remote.path(package, version))
