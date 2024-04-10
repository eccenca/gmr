"""Intelligent Model Registry (imr)"""
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
        file_path: Path = Path(directory) / package / version
        if not Path(file_path).exists():
            Path.mkdir(file_path, parents=True)
        with path.open() as fd, Path.open(file_path / "model.zip", "wb") as out:
            out.write(fd.read())
        shutil.unpack_archive(file_path / "model.zip", file_path / "model")

    def rm(self, package: str, version: str = "latest") -> None:
        """Remove a model from the remote repository."""
        artefact = self.repo + "/" + package
        if version is not None:
            artefact = self.repo + "/" + package + "/" + version
        path = ArtifactoryPath(artefact, auth=(self.user, self.password), auth_type=HTTPBasicAuth)
        if path.exists():
            path.unlink()

    def path(self, package: str, version: str = "latest") -> ArtifactoryPath:
        """Return the path to the model."""
        artefact = self.repo + "/" + package
        if version is not None:
            artefact += "/" + version
        return ArtifactoryPath(artefact, auth=(self.user, self.password), auth_type=HTTPBasicAuth)


class IMRLocal:
    """Local repository class."""

    repo: Path
    home: Path

    def __init__(self, repo: str | None = None):
        self.home = Path.home()
        if repo is None:
            self.repo = self.home / ".imr"
        else:
            self.repo = Path(repo)
        if not Path(self.repo).exists():
            Path(self.repo).mkdir(parents=True)

    def list(self) -> list[str]:
        """List local models.

        returns all the paths in the repository after main directory
        BASE/modela/version1
        BASE/modela/version2
        BASE/modelb/version3

        results in ["modela/version1", "modela/version2", "modelb/version3"]
        """
        return ["/".join(version.parts[-2:]) for version in self.repo.rglob("*/*/")]

    def push(self, directory: str, package: str, version: str = "latest") -> None:
        """Push a model in a directory to the local repository."""
        shutil.copytree(src=directory, dst=self.repo / package / version)

    def rm(self, package: str, version: str = "latest") -> None:
        """Remove a model from the local repository."""
        if version is None:
            shutil.rmtree(self.repo / package)
        else:
            shutil.rmtree(self.repo / package / version)

    def path(self, package: str, version: str = "latest") -> Path:
        """Return the path to the model."""
        path :Path = self.repo / package
        if version is not None:
            path = self.repo / package / version
        return path
