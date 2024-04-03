"""Example Test"""
from imr import dummy_function


def test_dummy() -> None:
    """Dummy Test"""
    assert dummy_function(1) == 2  # noqa: PLR2004
