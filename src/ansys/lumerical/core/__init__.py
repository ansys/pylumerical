"""
lumerical.

Core
"""



try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

from .lumapi import FDTD, MODE, INTERCONNECT, DEVICE, setLumericalInstallPath

__version__ = importlib_metadata.version(__name__.replace(".", "-"))
