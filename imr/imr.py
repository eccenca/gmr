# Inteligent Model Registry (imr)
import os
import shutil
from pathlib import Path

from artifactory import ArtifactoryPath
from requests.auth import HTTPBasicAuth


class IMRRemote:
    """Remote repository class."""

    def __init__(self, repo: str, user: str, password: str):
        self.repo = repo
        self.user = user
        self.password = password
        self.home = str(Path.home())

    def list(self) -> list:
        """List models from the remote repository."""
        path = ArtifactoryPath(self.repo, auth=(self.user, self.password), auth_type=HTTPBasicAuth)
        return [str(package).replace(self.repo + "/", "") for package in path.glob("*/*")]

    def push(self, directory: str, package: str, version: str = "latest") -> None:
        """Push a local model to the remote repository."""
        path = ArtifactoryPath(
            self.repo + "/" + package + "/" + version,
            auth=(self.user, self.password),
            auth_type=HTTPBasicAuth,
        )
        path.mkdir()
        shutil.make_archive("model", "zip", directory)
        path.deploy_file("model.zip")

    def pull(self, directory: str, package: str, version: str = "latest") -> None:
        """Pull a remote model to the local repository."""
        path = ArtifactoryPath(
            self.repo + "/" + package + "/" + version + "/model.zip",
            auth=(self.user, self.password),
            auth_type=HTTPBasicAuth,
        )
        file_path = directory + "/" + package + "/" + version
        if not Path(file_path).exists():
            Path.mkdir(file_path, parents=True)
        with path.open() as fd, Path.open(file_path + "/" + "model.zip", "wb") as out:
            out.write(fd.read())
        shutil.unpack_archive(file_path + "/" + "model.zip", file_path + "/model")

    def rm(self, package: str, version: str = "latest") -> None:
        """Remove a model from the remote repository."""
        artefact = self.repo + "/" + package
        if version is not None:
            artefact = self.repo + "/" + package + "/" + version
        path = ArtifactoryPath(artefact, auth=(self.user, self.password), auth_type=HTTPBasicAuth)
        if path.exists():
            path.unlink()


class IMRLocal:
    """Local repository class."""

    def __init__(self, repo: str | None = None):
        self.home = Path.home()
        if repo is None:
            self.repo = str(self.home) + "/.imr"
        else:
            self.repo = repo
        if not Path(self.repo).exists():
            Path.mkdir(self.repo, parents=True)

    def list(self) -> list:
        """List local models."""
        return [
            entry[0].replace(self.repo + "/", "")
            for entry in os.walk(self.repo)
            if len(entry[1]) == 0 and entry[0] not in self.repo
        ]

    def push(self, directory: str, package: str, version: str = "latest") -> None:
        """Push a model in a directory to the local repository."""
        shutil.copytree(directory, self.repo + "/" + package + "/" + version)

    def rm(self, package: str, version: str = "latest") -> None:
        """Remove a model from the local repository."""
        if version is None:
            shutil.rmtree(self.repo + "/" + package)
        else:
            shutil.rmtree(self.repo + "/" + package + "/" + version)
