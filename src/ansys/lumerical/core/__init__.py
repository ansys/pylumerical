"""
lumerical.

Core
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

from ansys.api.lumerical.lumapi import FDTD, MODE, INTERCONNECT, DEVICE, InteropPaths

InteropPaths.autoInitInstallPath()  # warns if the path cannot be guessed

__version__ = importlib_metadata.version(__name__.replace(".", "-"))
