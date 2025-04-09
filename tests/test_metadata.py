from ansys.lumerical.core import __version__


def test_pkg_version():
    import importlib.metadata as importlib_metadata

    assert importlib_metadata.version("ansys-lumerical-core") == __version__
