"""Unit test for package metadata."""
from ansys.lumerical.core import __version__


def test_pkg_version():
    """
    Verify that the package version defined in the code matches the version specified in the package metadata.

    Raises
    ------
        AssertionError: If the `__version__` does not match the version retrieved
                        from the package metadata.
    """
    import importlib.metadata as importlib_metadata

    # Read from the pyproject.toml
    # major, minor, patch
    read_version = importlib_metadata.version("ansys-lumerical-core")

    assert __version__ == read_version
