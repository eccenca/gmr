"""Repository tests."""

from imr.imr import IMRLocal
from tests import FIXTURE_DIR


def test_basic_list() -> None:
    """Test list items in repository."""
    number_of_models = 5
    directory = FIXTURE_DIR / "repository"
    repository = IMRLocal(repo=str(directory))
    models = repository.list()
    assert len(models) == number_of_models
    assert "modela/version1" in models
    assert "ignore-me" not in models
