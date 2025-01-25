from ansys.lumerical.library import __version__


def test_pkg_version():
    import importlib.metadata as importlib_metadata

    # Read from the pyproject.toml
    # major, minor, patch
    read_version = importlib_metadata.version("ansys-lumerical-library")

    assert __version__ == read_version
